import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func, and_, or_
from flask_babel import _

from models.doctor import DoctorModel
from models.doctor_specialty import DoctorSpecialtyModel
from utils import paginated_results, restrict_collector
from security import check


class Doctor(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('firstname', type=str)
    parser.add_argument('lastname', type=str)
    parser.add_argument('registry_number', type=str)
    parser.add_argument('document_number', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('specialty_list', type=list, location='json')

    @jwt_required()
    @check('doctor_get')
    @swag_from('../swagger/doctor/get_doctor.yaml')
    def get(self, id):
        doctor = DoctorModel.find_by_id(id)
        if doctor:
            return doctor.json()
        return {'message': _("DOCTOR_NOT_FOUND")}, 404

    @jwt_required()
    @check('doctor_update')
    @swag_from('../swagger/doctor/put_doctor.yaml')
    def put(self, id):
        doctor = DoctorModel.find_by_id(id)
        if doctor:
            newdata = Doctor.parser.parse_args()
            doctor_specialty_data_list = newdata['specialty_list']
            DoctorModel.from_reqparse(doctor, newdata)

            # doctor_specialt update
            doctor_specialty_list = []
            for doctor_specialty in doctor_specialty_data_list:
                if 'id' in doctor_specialty and doctor_specialty['id']:
                    doctor_specialty_model = DoctorSpecialtyModel.find_by_id(doctor_specialty['id'])
                    DoctorSpecialtyModel.from_reqparse(doctor_specialty_model, doctor_specialty)
                else:
                    doctor_specialty_model = DoctorSpecialtyModel(**doctor_specialty)
                doctor_specialty_list.append(doctor_specialty_model)

            doctor.specialty_list = doctor_specialty_list

            doctor.user_modify = get_jwt_identity()
            doctor.date_modify = datetime.now()
            doctor.save_to_db()
            return doctor.json()
        return {'message': _("DOCTOR_NOT_FOUND")}, 404

    @jwt_required()
    @check('doctor_delete')
    @swag_from('../swagger/doctor/delete_doctor.yaml')
    def delete(self, id):
        doctor = DoctorModel.find_by_id(id)
        if doctor:
            doctor.delete_from_db()

        return {'message': _("DOCTOR_DELETED")}


class DoctorList(Resource):

    @jwt_required()
    @check('doctor_list')
    @swag_from('../swagger/doctor/list_doctor.yaml')
    def get(self):
        query = DoctorModel.query
        return paginated_results(query)

    @jwt_required()
    @check('doctor_insert')
    @swag_from('../swagger/doctor/post_doctor.yaml')
    def post(self):
        data = Doctor.parser.parse_args()

        id = data.get('id')

        if id is not None and DoctorModel.find_by_id(id):
            return {'message': _("DOCTOR_DUPLICATED").format(id)}, 400

        doctor_specialty_data_list = data['specialty_list']
        del data['specialty_list']
        doctor = DoctorModel(**data)

        for doctor_specialty in doctor_specialty_data_list:
            doctor_specialty_model = DoctorSpecialtyModel(**doctor_specialty)
            doctor.specialty_list.append(doctor_specialty_model)

        try:
            doctor.user_create = get_jwt_identity()
            doctor.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating doctor.', exc_info=e)
            return {"message": _("DOCTOR_CREATE_ERROR")}, 500

        return doctor.json(), 201


class DoctorSearch(Resource):

    @jwt_required()
    @check('doctor_search')
    @swag_from('../swagger/doctor/search_doctor.yaml')
    def post(self):
        query = DoctorModel.query

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: DoctorModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'firstname', lambda x: func.lower(DoctorModel.firstname).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'lastname', lambda x: func.lower(DoctorModel.lastname).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'registry_number', lambda x: func.lower(DoctorModel.registry_number).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'document_number', lambda x: func.lower(DoctorModel.document_number).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_create',
                             lambda x: func.to_char(DoctorModel.date_create, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_create', lambda x: DoctorModel.user_create.contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_modify',
                             lambda x: func.to_char(DoctorModel.date_modify, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_modify', lambda x: DoctorModel.user_modify.contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'origin', lambda x: func.lower(DoctorModel.origin).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
