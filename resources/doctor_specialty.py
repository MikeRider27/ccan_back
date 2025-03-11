import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.doctor_specialty import DoctorSpecialtyModel
from security import check
from utils import restrict, paginated_results


class DoctorSpecialty(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('specialty_id', type=int)

    @jwt_required()
    @check('doctor_specialty_get')
    @swag_from('../swagger/doctor_specialty/get_doctor_specialty.yaml')
    def get(self, id):
        doctor_specialty = DoctorSpecialtyModel.find_by_id(id)
        if doctor_specialty:
            return doctor_specialty.json()
        return {'message': _("DOCTOR_SPECIALITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('doctor_specialty_update')
    @swag_from('../swagger/doctor_specialty/put_doctor_specialty.yaml')
    def put(self, id):
        doctor_specialty = DoctorSpecialtyModel.find_by_id(id)
        if doctor_specialty:
            newdata = DoctorSpecialty.parser.parse_args()
            DoctorSpecialtyModel.from_reqparse(doctor_specialty, newdata)
            doctor_specialty.save_to_db()
            return doctor_specialty.json()
        return {'message': _("DOCTOR_SPECIALITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('doctor_specialty_delete')
    @swag_from('../swagger/doctor_specialty/delete_doctor_specialty.yaml')
    def delete(self, id):
        doctor_specialty = DoctorSpecialtyModel.find_by_id(id)
        if doctor_specialty:
            doctor_specialty.delete_from_db()

        return {'message': _("DOCTOR_SPECIALITY_DELETED")}


class DoctorSpecialtyList(Resource):

    @jwt_required()
    @check('doctor_specialty_list')
    @swag_from('../swagger/doctor_specialty/list_doctor_specialty.yaml')
    def get(self):
        query = DoctorSpecialtyModel.query
        return paginated_results(query)

    @jwt_required()
    @check('doctor_specialty_insert')
    @swag_from('../swagger/doctor_specialty/post_doctor_specialty.yaml')
    def post(self):
        data = DoctorSpecialty.parser.parse_args()

        id = data.get('id')

        if id is not None and DoctorSpecialtyModel.find_by_id(id):
            return {'message': _("DOCTOR_SPECIALITY_DUPLICATED").format(id)}, 400

        doctor_specialty = DoctorSpecialtyModel(**data)
        try:
            doctor_specialty.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating doctor speciality.', exc_info=e)
            return {"message": _("DOCTOR_SPECIALITY_CREATE_ERROR")}, 500

        return doctor_specialty.json(), 201


class DoctorSpecialtySearch(Resource):

    @jwt_required()
    @check('doctor_specialty_search')
    @swag_from('../swagger/doctor_specialty/search_doctor_specialty.yaml')
    def post(self):
        query = DoctorSpecialtyModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: DoctorSpecialtyModel.id == x)
            query = restrict(query, filters, 'doctor_id', lambda x: DoctorSpecialtyModel.doctor_id == x)
            query = restrict(query, filters, 'specialty_id', lambda x: DoctorSpecialtyModel.specialty_id == x)
        return paginated_results(query)
