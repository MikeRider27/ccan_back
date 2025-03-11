import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.patient_hospital import PatientHospitalModel
from utils import restrict, paginated_results
from security import check


class PatientHospital(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('hospital_id', type=int)

    @jwt_required()
    @check('patient_hospital_get')
    @swag_from('../swagger/patient_hospital/get_patient_hospital.yaml')
    def get(self, id):
        patient_hospital = PatientHospitalModel.find_by_id(id)
        if patient_hospital:
            return patient_hospital.json()
        return {'message': _("PATIENT_HOSPITAL_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_hospital_update')
    @swag_from('../swagger/patient_hospital/put_patient_hospital.yaml')
    def put(self, id):
        patient_hospital = PatientHospitalModel.find_by_id(id)
        if patient_hospital:
            newdata = PatientHospital.parser.parse_args()
            PatientHospitalModel.from_reqparse(patient_hospital, newdata)
            patient_hospital.save_to_db()
            return patient_hospital.json()
        return {'message': _("PATIENT_HOSPITAL_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_hospital_delete')
    @swag_from('../swagger/patient_hospital/delete_patient_hospital.yaml')
    def delete(self, id):
        patient_hospital = PatientHospitalModel.find_by_id(id)
        if patient_hospital:
            patient_hospital.delete_from_db()

        return {'message': _("PATIENT_HOSPITAL_DELETED")}


class PatientHospitalList(Resource):

    @jwt_required()
    @check('patient_hospital_list')
    @swag_from('../swagger/patient_hospital/list_patient_hospital.yaml')
    def get(self):
        query = PatientHospitalModel.query
        return paginated_results(query)

    @jwt_required()
    @check('patient_hospital_insert')
    @swag_from('../swagger/patient_hospital/post_patient_hospital.yaml')
    def post(self):
        data = PatientHospital.parser.parse_args()

        id = data.get('id')

        if id is not None and PatientHospitalModel.find_by_id(id):
            return {'message': _("PATIENT_HOSPITAL_DUPLICATED").format(id)}, 400

        patient_hospital = PatientHospitalModel(**data)
        try:
            patient_hospital.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating patient hospital.', exc_info=e)
            return {"message": _("PATIENT_HOSPITAL_CREATE_ERROR")}, 500

        return patient_hospital.json(), 201


class PatientHospitalSearch(Resource):

    @jwt_required()
    @check('patient_hospital_search')
    @swag_from('../swagger/patient_hospital/search_patient_hospital.yaml')
    def post(self):
        query = PatientHospitalModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PatientHospitalModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: PatientHospitalModel.patient_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: PatientHospitalModel.hospital_id == x)

        # default order
        query = query.order_by(PatientHospitalModel.id.desc())
        return paginated_results(query)
