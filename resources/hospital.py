import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.hospital import HospitalModel
from utils import restrict, paginated_results
from security import check


class Hospital(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('country_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('system', type=bool)
    parser.add_argument('hospital_codigo', type=str)

    @jwt_required()
    @check('hospital_get')
    @swag_from('../swagger/hospital/get_hospital.yaml')
    def get(self, id):
        hospital = HospitalModel.find_by_id(id)
        if hospital:
            return hospital.json()
        return {'message': _("HOSPITAL_NOT_FOUND")}, 404

    @jwt_required()
    @check('hospital_update')
    @swag_from('../swagger/hospital/put_hospital.yaml')
    def put(self, id):
        hospital = HospitalModel.find_by_id(id)
        if hospital:
            newdata = Hospital.parser.parse_args()
            HospitalModel.from_reqparse(hospital, newdata)

            hospital.user_modify = get_jwt_identity()
            hospital.date_modify = datetime.now()
            hospital.save_to_db()
            return hospital.json()
        return {'message': _("HOSPITAL_NOT_FOUND")}, 404

    @jwt_required()
    @check('hospital_delete')
    @swag_from('../swagger/hospital/delete_hospital.yaml')
    def delete(self, id):
        hospital = HospitalModel.find_by_id(id)
        if hospital:
            hospital.delete_from_db()

        return {'message': _("HOSPITAL_DELETED")}


class HospitalList(Resource):

    @jwt_required()
    @check('hospital_list')
    @swag_from('../swagger/hospital/list_hospital.yaml')
    def get(self):
        query = HospitalModel.query
        return paginated_results(query)

    @jwt_required()
    @check('hospital_insert')
    @swag_from('../swagger/hospital/post_hospital.yaml')
    def post(self):
        data = Hospital.parser.parse_args()

        id = data.get('id')

        if id is not None and HospitalModel.find_by_id(id):
            return {'message': _("HOSPITAL_DUPLICATED").format(id)}, 400

        hospital = HospitalModel(**data)
        try:
            hospital.user_create = get_jwt_identity()
            hospital.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating hospital.', exc_info=e)
            return {"message": _("HOSPITAL_CREATE_ERROR")}, 500

        return hospital.json(), 201


class HospitalSearch(Resource):

    @jwt_required()
    @check('hospital_search')
    @swag_from('../swagger/hospital/search_hospital.yaml')
    def post(self):
        query = HospitalModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: HospitalModel.id == x)
            query = restrict(query, filters, 'description', lambda x: func.lower(HospitalModel.description).contains(func.lower(x)))
            query = restrict(query, filters, 'country_id', lambda x: HospitalModel.country_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(HospitalModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: HospitalModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(HospitalModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: HospitalModel.user_modify.contains(x))
            query = restrict(query, filters, 'system', lambda x: HospitalModel.system == x)

        return paginated_results(query)
