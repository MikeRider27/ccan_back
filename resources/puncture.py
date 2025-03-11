import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.puncture import PunctureModel
from utils import restrict, paginated_results
from security import check


class Puncture(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('observation', type=str)
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('puncture_get')
    @swag_from('../swagger/puncture/get_puncture.yaml')
    def get(self, id):
        puncture = PunctureModel.find_by_id(id)
        if puncture:
            return puncture.json()
        return {'message': _("PUNCTURE_NOT_FOUND")}, 404

    @jwt_required()
    @check('puncture_update')
    @swag_from('../swagger/puncture/put_puncture.yaml')
    def put(self, id):
        puncture = PunctureModel.find_by_id(id)
        if puncture:
            newdata = Puncture.parser.parse_args()
            PunctureModel.from_reqparse(puncture, newdata)

            puncture.user_modify = get_jwt_identity()
            puncture.date_modify = datetime.now()
            puncture.save_to_db()
            return puncture.json()
        return {'message': _("PUNCTURE_NOT_FOUND")}, 404

    @jwt_required()
    @check('puncture_delete')
    @swag_from('../swagger/puncture/delete_puncture.yaml')
    def delete(self, id):
        puncture = PunctureModel.find_by_id(id)
        if puncture:
            puncture.delete_from_db()

        return {'message': _("PUNCTURE_DELETED")}


class PunctureList(Resource):

    @jwt_required()
    @check('puncture_list')
    @swag_from('../swagger/puncture/list_puncture.yaml')
    def get(self):
        query = PunctureModel.query
        return paginated_results(query)

    @jwt_required()
    @check('puncture_insert')
    @swag_from('../swagger/puncture/post_puncture.yaml')
    def post(self):
        data = Puncture.parser.parse_args()

        id = data.get('id')

        if id is not None and PunctureModel.find_by_id(id):
            return {'message': _("PUNCTURE_DUPLICATED").format(id)}, 400

        puncture = PunctureModel(**data)
        try:
            puncture.user_create = get_jwt_identity()
            puncture.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating puncture.', exc_info=e)
            return {"message": _("PUNCTURE_CREATE_ERROR")}, 500

        return puncture.json(), 201


class PunctureSearch(Resource):

    @jwt_required()
    @check('puncture_search')
    @swag_from('../swagger/puncture/search_puncture.yaml')
    def post(self):
        query = PunctureModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PunctureModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: PunctureModel.patient_id == x)
            query = restrict(query, filters, 'observation', lambda x: PunctureModel.observation.contains(x))
            query = restrict(query, filters, 'doctor_id', lambda x: PunctureModel.doctor_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: PunctureModel.hospital_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(PunctureModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: PunctureModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(PunctureModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: PunctureModel.user_modify.contains(x))

        return paginated_results(query)
