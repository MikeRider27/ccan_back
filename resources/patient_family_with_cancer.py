import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy import func

from models.patient_family_with_cancer import PatientFamilyWithCancerModel
from utils import restrict, paginated_results
from security import check


class PatientFamilyWithCancer(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('personal_pathological_history_id', type=int)
    parser.add_argument('family_id', type=int)
    parser.add_argument('family_vital_state_id', type=int)
    parser.add_argument('cancer_type', type=str)

    @jwt_required()
    @check('patient_family_with_cancer_get')
    @swag_from('../swagger/patient_family_with_cancer/get_patient_family_with_cancer.yaml')
    def get(self, id):
        patient_family_with_cancer = PatientFamilyWithCancerModel.find_by_id(id)
        if patient_family_with_cancer:
            return patient_family_with_cancer.json()
        return {'message': _("PATIENT_FAMILY_WITH_CANCER_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_family_with_cancer_update')
    @swag_from('../swagger/patient_family_with_cancer/put_patient_family_with_cancer.yaml')
    def put(self, id):
        patient_family_with_cancer = PatientFamilyWithCancerModel.find_by_id(id)
        if patient_family_with_cancer:
            newdata = PatientFamilyWithCancer.parser.parse_args()
            PatientFamilyWithCancerModel.from_reqparse(patient_family_with_cancer, newdata)
            patient_family_with_cancer.save_to_db()
            return patient_family_with_cancer.json()
        return {'message': _("PATIENT_FAMILY_WITH_CANCER_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_family_with_cancer_delete')
    @swag_from('../swagger/patient_family_with_cancer/delete_patient_family_with_cancer.yaml')
    def delete(self, id):
        patient_family_with_cancer = PatientFamilyWithCancerModel.find_by_id(id)
        if patient_family_with_cancer:
            patient_family_with_cancer.delete_from_db()

        return {'message': _("PATIENT_FAMILY_WITH_CANCER_DELETED")}


class PatientFamilyWithCancerList(Resource):

    @jwt_required()
    @check('patient_family_with_cancer_list')
    @swag_from('../swagger/patient_family_with_cancer/list_patient_family_with_cancer.yaml')
    def get(self):
        query = PatientFamilyWithCancerModel.query
        return paginated_results(query)

    @jwt_required()
    @check('patient_family_with_cancer_insert')
    @swag_from('../swagger/patient_family_with_cancer/post_patient_family_with_cancer.yaml')
    def post(self):
        data = PatientFamilyWithCancer.parser.parse_args()

        id = data.get('id')

        if id is not None and PatientFamilyWithCancerModel.find_by_id(id):
            return {'message': _("PATIENT_FAMILY_WITH_CANCER_DUPLICATED").format(id)}, 400

        patient_family_with_cancer = PatientFamilyWithCancerModel(**data)
        try:
            patient_family_with_cancer.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating patient family with cancer.', exc_info=e)
            return {"message": _("PATIENT_FAMILY_WITH_CANCER_CREATE_ERROR")}, 500

        return patient_family_with_cancer.json(), 201


class PatientFamilyWithCancerSearch(Resource):

    @jwt_required()
    @check('patient_family_with_cancer_search')
    @swag_from('../swagger/patient_family_with_cancer/search_patient_family_with_cancer.yaml')
    def post(self):
        query = PatientFamilyWithCancerModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PatientFamilyWithCancerModel.id == x)
            query = restrict(query, filters, 'personal_pathological_history_id', lambda x: PatientFamilyWithCancerModel.personal_pathological_history_id == x)
            query = restrict(query, filters, 'family_id', lambda x: PatientFamilyWithCancerModel.family_id == x)
            query = restrict(query, filters, 'family_vital_state_id', lambda x: PatientFamilyWithCancerModel.family_vital_state_id == x)
            query = restrict(query, filters, 'cancer_type', lambda x: func.lower(PatientFamilyWithCancerModel.cancer_type).contains(func.lower(x)))
        return paginated_results(query)
