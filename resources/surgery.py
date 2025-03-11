import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.medical_team import MedicalTeamModel
from models.surgery import SurgeryModel
from utils import restrict, paginated_results
from security import check


class Surgery(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('observation', type=str)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('medical_team', type=list, location='json')
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('surgical_technique', type=str)

    @jwt_required()
    @check('surgery_get')
    @swag_from('../swagger/surgery/get_surgery.yaml')
    def get(self, id):
        surgery = SurgeryModel.find_by_id(id)
        if surgery:
            return surgery.json()
        return {'message': _("SURGERY_NOT_FOUND")}, 404

    @jwt_required()
    @check('surgery_update')
    @swag_from('../swagger/surgery/put_surgery.yaml')
    def put(self, id):
        surgery = SurgeryModel.find_by_id(id)
        if surgery:
            newdata = Surgery.parser.parse_args()
            medical_team_data_list = newdata['medical_team']
            SurgeryModel.from_reqparse(surgery, newdata)

            # medical_team update
            medical_team_list = []
            for medical_team in medical_team_data_list:
                if 'id' in medical_team and medical_team['id']:
                    medical_team_model = MedicalTeamModel.find_by_id(medical_team['id'])
                    MedicalTeamModel.from_reqparse(medical_team_model, medical_team)
                else:
                    medical_team['id'] = None
                    medical_team_model = MedicalTeamModel(**medical_team)
                medical_team_list.append(medical_team_model)

            surgery.medical_team = medical_team_list

            surgery.user_modify = get_jwt_identity()
            surgery.date_modify = datetime.now()
            surgery.save_to_db()
            return surgery.json()
        return {'message': _("SURGERY_NOT_FOUND")}, 404

    @jwt_required()
    @check('surgery_delete')
    @swag_from('../swagger/surgery/delete_surgery.yaml')
    def delete(self, id):
        surgery = SurgeryModel.find_by_id(id)
        if surgery:
            surgery.delete_from_db()

        return {'message': _("SURGERY_DELETED")}


class SurgeryList(Resource):

    @jwt_required()
    @check('surgery_list')
    @swag_from('../swagger/surgery/list_surgery.yaml')
    def get(self):
        query = SurgeryModel.query
        return paginated_results(query)

    @jwt_required()
    @check('surgery_insert')
    @swag_from('../swagger/surgery/post_surgery.yaml')
    def post(self):
        data = Surgery.parser.parse_args()

        id = data.get('id')

        if id is not None and SurgeryModel.find_by_id(id):
            return {'message': _("SURGERY_DUPLICATED").format(id)}, 400

        medical_team_data_list = data['medical_team']
        del data['medical_team']
        surgery = SurgeryModel(**data)

        for medical_team in medical_team_data_list:
            medical_team['id'] = None
            medical_team_model = MedicalTeamModel(**medical_team)
            surgery.medical_team.append(medical_team_model)

        try:
            surgery.user_create = get_jwt_identity()
            surgery.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating surgery.', exc_info=e)
            return {"message": _("SURGERY_CREATE_ERROR")}, 500

        return surgery.json(), 201


class SurgerySearch(Resource):

    @jwt_required()
    @check('surgery_search')
    @swag_from('../swagger/surgery/search_surgery.yaml')
    def post(self):
        query = SurgeryModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: SurgeryModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: SurgeryModel.patient_id == x)
            query = restrict(query, filters, 'observation', lambda x: SurgeryModel.observation.contains(x))
            query = restrict(query, filters, 'hospital_id', lambda x: SurgeryModel.hospital_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(SurgeryModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: SurgeryModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(SurgeryModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: SurgeryModel.user_modify.contains(x))
            query = restrict(query, filters, 'surgical_technique', lambda x: SurgeryModel.observation.contains(x))

        # default order
        query = query.order_by(SurgeryModel.id.desc())

        return paginated_results(query)
