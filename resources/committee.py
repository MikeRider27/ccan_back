import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.committee import CommitteeModel
from models.medical_committee import MedicalCommitteeModel
from security import check
from utils import restrict, paginated_results


class Committee(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('observation', type=str)
    parser.add_argument('committee_team', type=list, location='json')
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('committee_get')
    @swag_from('../swagger/committee/get_committee.yaml')
    def get(self, id):
        committee = CommitteeModel.find_by_id(id)
        if committee:
            return committee.json()
        return {'message': _("COMMITTEE_NOT_FOUND")}, 404

    @jwt_required()
    @check('committee_update')
    @swag_from('../swagger/committee/put_committee.yaml')
    def put(self, id):
        committee = CommitteeModel.find_by_id(id)
        if committee:
            newdata = Committee.parser.parse_args()
            medical_committee_data_list = newdata['committee_team']
            CommitteeModel.from_reqparse(committee, newdata)

            # medical_committee update
            medical_committee_list = []
            for medical_committee in medical_committee_data_list:
                if 'id' in medical_committee and medical_committee['id']:
                    medical_committee_model = MedicalCommitteeModel.find_by_id(medical_committee['id'])
                    MedicalCommitteeModel.from_reqparse(medical_committee_model, medical_committee)
                else:
                    medical_committee['id'] = None
                    medical_team_model = MedicalCommitteeModel(**medical_committee)
                medical_committee_list.append(medical_committee)

            committee.medical_committee = medical_committee_list

            committee.user_modify = get_jwt_identity()
            committee.date_modify = datetime.now()
            committee.save_to_db()
            return committee.json()
        return {'message':  _("COMMITTEE_NOT_FOUND")}, 404

    @jwt_required()
    @check('committee_delete')
    @swag_from('../swagger/committee/delete_committee.yaml')
    def delete(self, id):
        committee = CommitteeModel.find_by_id(id)
        if committee:
            committee.delete_from_db()

        return {'message': _("COMMITTEE_DELETED")}


class CommitteeList(Resource):

    @jwt_required()
    @check('committee_list')
    @swag_from('../swagger/committee/list_committee.yaml')
    def get(self):
        query = CommitteeModel.query
        return paginated_results(query)

    @jwt_required()
    @check('committee_insert')
    @swag_from('../swagger/committee/post_committee.yaml')
    def post(self):
        data = Committee.parser.parse_args()

        id = data.get('id')

        if id is not None and CommitteeModel.find_by_id(id):
            return {'message': _("COMMITTEE_DUPLICATED").format(id)}, 400

        medical_committee_data_list = data['committee_team']
        del data['committee_team']
        committee = CommitteeModel(**data)

        for medical_committee in medical_committee_data_list:
            medical_committee['id'] = None
            medical_committee_model = MedicalCommitteeModel(**medical_committee)
            committee.committee_team.append(medical_committee_model)

        try:
            committee.user_create = get_jwt_identity()
            committee.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating committee', exc_info=e)
            return {"message": _("COMMITTEE_CREATE_ERROR")}, 500

        return committee.json(), 201


class CommitteeSearch(Resource):

    @jwt_required()
    @check('committee_search')
    @swag_from('../swagger/committee/search_committee.yaml')
    def post(self):
        query = CommitteeModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: CommitteeModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: CommitteeModel.patient_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: CommitteeModel.hospital_id == x)
            query = restrict(query, filters, 'observation', lambda x: CommitteeModel.observation.contains(x))
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(CommitteeModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: CommitteeModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(CommitteeModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: CommitteeModel.user_modify.contains(x))

        return paginated_results(query)
