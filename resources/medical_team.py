import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.medical_team import MedicalTeamModel
from utils import restrict, paginated_results
from security import check


class MedicalTeam(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('surgery_id', type=int)
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('rol', type=str)
    parser.add_argument('nurse', type=str)
    parser.add_argument('anesthetist', type=str)
    parser.add_argument('surgical_instrumentator', type=str)
    parser.add_argument('technical', type=str)

    @jwt_required()
    @check('medical_team_get')
    @swag_from('../swagger/medical_team/get_medical_team.yaml')
    def get(self, id):
        medical_team = MedicalTeamModel.find_by_id(id)
        if medical_team:
            return medical_team.json()
        return {'message': _("MEDICAL_TEAM_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_team_update')
    @swag_from('../swagger/medical_team/put_medical_team.yaml')
    def put(self, id):
        medical_team = MedicalTeamModel.find_by_id(id)
        if medical_team:
            newdata = MedicalTeam.parser.parse_args()
            MedicalTeamModel.from_reqparse(medical_team, newdata)
            medical_team.save_to_db()
            return medical_team.json()
        return {'message': _("MEDICAL_TEAM_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_team_delete')
    @swag_from('../swagger/medical_team/delete_medical_team.yaml')
    def delete(self, id):
        medical_team = MedicalTeamModel.find_by_id(id)
        if medical_team:
            medical_team.delete_from_db()

        return {'message': _("MEDICAL_TEAM_DELETED")}


class MedicalTeamList(Resource):

    @jwt_required()
    @check('medical_team_list')
    @swag_from('../swagger/medical_team/list_medical_team.yaml')
    def get(self):
        query = MedicalTeamModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medical_team_insert')
    @swag_from('../swagger/medical_team/post_medical_team.yaml')
    def post(self):
        data = MedicalTeam.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicalTeamModel.find_by_id(id):
            return {'message': _("MEDICAL_TEAM_DUPLICATED").format(id)}, 400

        medical_team = MedicalTeamModel(**data)
        try:
            medical_team.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating medical team.', exc_info=e)
            return {"message": _("MEDICAL_TEAM_CREATE_ERROR")}, 500

        return medical_team.json(), 201


class MedicalTeamSearch(Resource):

    @jwt_required()
    @check('medical_team_search')
    @swag_from('../swagger/medical_team/search_medical_team.yaml')
    def post(self):
        query = MedicalTeamModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MedicalTeamModel.id == x)
            query = restrict(query, filters, 'surgery_id', lambda x: MedicalTeamModel.surgery_id == x)
            query = restrict(query, filters, 'doctor_id', lambda x: MedicalTeamModel.doctor_id == x)
            query = restrict(query, filters, 'rol', lambda x: MedicalTeamModel.rol.contains(x))
            query = restrict(query, filters, 'nurse', lambda x: MedicalTeamModel.rol.contains(x))
            query = restrict(query, filters, 'anesthetist', lambda x: MedicalTeamModel.rol.contains(x))
            query = restrict(query, filters, 'surgical_instrumentator', lambda x: MedicalTeamModel.rol.contains(x))
            query = restrict(query, filters, 'technical', lambda x: MedicalTeamModel.rol.contains(x))

        # default order
        query = query.order_by(MedicalTeamModel.id.desc())

        return paginated_results(query)
