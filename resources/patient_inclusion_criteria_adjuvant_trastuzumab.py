import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.patient_inclusion_criteria_adjuvant_trastuzumab import PatientInclusionCriteriaAdjuvantTrastuzumabModel
from security import check
from utils import restrict, paginated_results


class PatientInclusionCriteriaAdjuvantTrastuzumab(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('diagnosed_invasive_adenocarcinoma', type=bool)
    parser.add_argument('adenocarcinoma_completely_resected', type=bool)
    parser.add_argument('tumor_diameter_greater_10mm', type=bool)
    parser.add_argument('adjuvant_trastuzumab_her2_positive', type=bool)
    parser.add_argument('her2_positive_id', type=dict, location='json')
    parser.add_argument('determination_hormone_receptors', type=bool)
    parser.add_argument('absolute_neutrophils_eq_greater_1500_ul', type=bool)
    parser.add_argument('platelets_eq_greater_90000_mm3', type=bool)
    parser.add_argument('renal_hepatic_appropriate', type=bool)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('patient_inclusion_criteria_adjuvant_trastuzumab_get')
    @swag_from('../swagger/patient_inclusion_criteria_adjuvant_trastuzumab/get_patient_inclusion_criteria_adjuvant_trastuzumab.yaml')
    def get(self, id):
        patient_inclusion_criteria_adjuvant_trastuzumab = PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(id)
        if patient_inclusion_criteria_adjuvant_trastuzumab:
            return patient_inclusion_criteria_adjuvant_trastuzumab.json()
        return {'message': _("PATIENT_INCLUSION_CRITERIA_ADJUVANT_TRASTUZUMAB_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_inclusion_criteria_adjuvant_trastuzumab_update')
    @swag_from('../swagger/patient_inclusion_criteria_adjuvant_trastuzumab/put_patient_inclusion_criteria_adjuvant_trastuzumab.yaml')
    def put(self, id):
        patient_inclusion_criteria_adjuvant_trastuzumab = PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(id)
        if patient_inclusion_criteria_adjuvant_trastuzumab:
            newdata = PatientInclusionCriteriaAdjuvantTrastuzumab.parser.parse_args()
            PatientInclusionCriteriaAdjuvantTrastuzumabModel.from_reqparse(patient_inclusion_criteria_adjuvant_trastuzumab, newdata)

            patient_inclusion_criteria_adjuvant_trastuzumab.user_modify = get_jwt_identity()
            patient_inclusion_criteria_adjuvant_trastuzumab.date_modify = datetime.now()
            patient_inclusion_criteria_adjuvant_trastuzumab.save_to_db()
            return patient_inclusion_criteria_adjuvant_trastuzumab.json()
        return {'message': _("PATIENT_INCLUSION_CRITERIA_ADJUVANT_TRASTUZUMAB_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_inclusion_criteria_adjuvant_trastuzumab_delete')
    @swag_from('../swagger/patient_inclusion_criteria_adjuvant_trastuzumab/delete_patient_inclusion_criteria_adjuvant_trastuzumab.yaml')
    def delete(self, id):
        patient_inclusion_criteria_adjuvant_trastuzumab = PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(id)
        if patient_inclusion_criteria_adjuvant_trastuzumab:
            patient_inclusion_criteria_adjuvant_trastuzumab.delete_from_db()

        return {'message': _("PATIENT_INCLUSION_CRITERIA_ADJUVANT_TRASTUZUMAB_DELETED")}


class PatientInclusionCriteriaAdjuvantTrastuzumabList(Resource):

    @jwt_required()
    @check('patient_inclusion_criteria_adjuvant_trastuzumab_list')
    @swag_from('../swagger/patient_inclusion_criteria_adjuvant_trastuzumab/list_patient_inclusion_criteria_adjuvant_trastuzumab.yaml')
    def get(self):
        query = PatientInclusionCriteriaAdjuvantTrastuzumabModel.query
        return paginated_results(query)

    @jwt_required()
    @check('patient_inclusion_criteria_adjuvant_trastuzumab_insert')
    @swag_from('../swagger/patient_inclusion_criteria_adjuvant_trastuzumab/post_patient_inclusion_criteria_adjuvant_trastuzumab.yaml')
    def post(self):
        data = PatientInclusionCriteriaAdjuvantTrastuzumab.parser.parse_args()

        id = data.get('id')

        if id is not None and PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(id):
            return {'message': _("PATIENT_INCLUSION_CRITERIA_ADJUVANT_TRASTUZUMAB_DUPLICATED").format(id)}, 400

        patient_inclusion_criteria_adjuvant_trastuzumab = PatientInclusionCriteriaAdjuvantTrastuzumabModel(**data)
        try:
            patient_inclusion_criteria_adjuvant_trastuzumab.user_create = get_jwt_identity()
            patient_inclusion_criteria_adjuvant_trastuzumab.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating patiend inclusion criteria adjuvant trastuzumab.', exc_info=e)
            return {"message": _("PATIENT_INCLUSION_CRITERIA_ADJUVANT_TRASTUZUMAB_CREATE_ERROR")}, 500

        return patient_inclusion_criteria_adjuvant_trastuzumab.json(), 201


class PatientInclusionCriteriaAdjuvantTrastuzumabSearch(Resource):

    @jwt_required()
    @check('patient_inclusion_criteria_adjuvant_trastuzumab_search')
    @swag_from('../swagger/patient_inclusion_criteria_adjuvant_trastuzumab/search_patient_inclusion_criteria_adjuvant_trastuzumab.yaml')
    def post(self):
        query = PatientInclusionCriteriaAdjuvantTrastuzumabModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PatientInclusionCriteriaAdjuvantTrastuzumabModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: PatientInclusionCriteriaAdjuvantTrastuzumabModel.patient_id == x)
            query = restrict(query, filters, 'diagnosed_invasive_adenocarcinoma', lambda x: x)
            query = restrict(query, filters, 'adenocarcinoma_completely_resected', lambda x: x)
            query = restrict(query, filters, 'tumor_diameter_greater_10mm', lambda x: x)
            query = restrict(query, filters, 'adjuvant_trastuzumab_her2_positive', lambda x: x)
            query = restrict(query, filters, 'determination_hormone_receptors', lambda x: x)
            query = restrict(query, filters, 'absolute_neutrophils_eq_greater_1500_ul', lambda x: x)
            query = restrict(query, filters, 'platelets_eq_greater_90000_mm3', lambda x: x)
            query = restrict(query, filters, 'renal_hepatic_appropriate', lambda x: x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(PatientInclusionCriteriaAdjuvantTrastuzumabModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: PatientInclusionCriteriaAdjuvantTrastuzumabModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(PatientInclusionCriteriaAdjuvantTrastuzumabModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: PatientInclusionCriteriaAdjuvantTrastuzumabModel.user_modify.contains(x))
        return paginated_results(query)
