import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.patient_inclusion_criteria_neoadjuvant_trastuzumab import PatientInclusionCriteriaNeoadjuvantTrastuzumabModel
from security import check
from utils import restrict, paginated_results


class PatientInclusionCriteriaNeoadjuvantTrastuzumab(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('diagnosed_invasive_adenocarcinoma', type=bool)
    parser.add_argument('neoadjuvant_trastuzumab_her2_positive', type=bool)
    parser.add_argument('her2_positive_id', type=dict, location='json')
    parser.add_argument('determination_hormone_receptors', type=bool)
    parser.add_argument('tumor_eq_ge_2cm', type=bool)
    parser.add_argument('positive_axilla', type=bool)
    parser.add_argument('marked_tumor_bed', type=bool)
    parser.add_argument('blood_count_renal_hepatic_appropriate', type=bool)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('tumor_size_diameter_determined_by', type=bool)
    parser.add_argument('positive_armpit_determined_by', type=bool)

    @jwt_required()
    @check('patient_inclusion_criteria_neoadjuvant_trastuzumab_get')
    @swag_from('../swagger/patient_inclusion_criteria_neoadjuvant_trastuzumab/get_patient_inclusion_criteria_neoadjuvant_trastuzumab.yaml')
    def get(self, id):
        patient_inclusion_criteria_neoadjuvant_trastuzumab = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(id)
        if patient_inclusion_criteria_neoadjuvant_trastuzumab:
            return patient_inclusion_criteria_neoadjuvant_trastuzumab.json()
        return {'message': _("PATIENT_INCLUSION_CRITERIA_NEOADJUVANT_TRASTUZUMAB_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_inclusion_criteria_neoadjuvant_trastuzumab_update')
    @swag_from('../swagger/patient_inclusion_criteria_neoadjuvant_trastuzumab/put_patient_inclusion_criteria_neoadjuvant_trastuzumab.yaml')
    def put(self, id):
        patient_inclusion_criteria_neoadjuvant_trastuzumab = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(id)
        if patient_inclusion_criteria_neoadjuvant_trastuzumab:
            newdata = PatientInclusionCriteriaNeoadjuvantTrastuzumab.parser.parse_args()
            PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.from_reqparse(patient_inclusion_criteria_neoadjuvant_trastuzumab, newdata)

            patient_inclusion_criteria_neoadjuvant_trastuzumab.user_modify = get_jwt_identity()
            patient_inclusion_criteria_neoadjuvant_trastuzumab.date_modify = datetime.now()
            patient_inclusion_criteria_neoadjuvant_trastuzumab.save_to_db()
            return patient_inclusion_criteria_neoadjuvant_trastuzumab.json()
        return {'message': _("PATIENT_INCLUSION_CRITERIA_NEOADJUVANT_TRASTUZUMAB_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_inclusion_criteria_neoadjuvant_trastuzumab_delete')
    @swag_from('../swagger/patient_inclusion_criteria_neoadjuvant_trastuzumab/delete_patient_inclusion_criteria_neoadjuvant_trastuzumab.yaml')
    def delete(self, id):
        patient_inclusion_criteria_neoadjuvant_trastuzumab = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(id)
        if patient_inclusion_criteria_neoadjuvant_trastuzumab:
            patient_inclusion_criteria_neoadjuvant_trastuzumab.delete_from_db()

        return {'message': _("PATIENT_INCLUSION_CRITERIA_NEOADJUVANT_TRASTUZUMAB_DELETED")}


class PatientInclusionCriteriaNeoadjuvantTrastuzumabList(Resource):

    @jwt_required()
    @check('patient_inclusion_criteria_neoadjuvant_trastuzumab_list')
    @swag_from('../swagger/patient_inclusion_criteria_neoadjuvant_trastuzumab/list_patient_inclusion_criteria_neoadjuvant_trastuzumab.yaml')
    def get(self):
        query = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.query
        return paginated_results(query)

    @jwt_required()
    @check('patient_inclusion_criteria_neoadjuvant_trastuzumab_insert')
    @swag_from('../swagger/patient_inclusion_criteria_neoadjuvant_trastuzumab/post_patient_inclusion_criteria_neoadjuvant_trastuzumab.yaml')
    def post(self):
        data = PatientInclusionCriteriaNeoadjuvantTrastuzumab.parser.parse_args()

        id = data.get('id')

        if id is not None and PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(id):
            return {'message': _("PATIENT_INCLUSION_CRITERIA_NEOADJUVANT_TRASTUZUMAB_DUPLICATED").format(id)}, 400

        patient_inclusion_criteria_neoadjuvant_trastuzumab = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel(**data)
        try:
            patient_inclusion_criteria_neoadjuvant_trastuzumab.user_create = get_jwt_identity()
            patient_inclusion_criteria_neoadjuvant_trastuzumab.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating patient inclusion criteria neoadjuvant trastuzumab.', exc_info=e)
            return {"message": _("PATIENT_INCLUSION_CRITERIA_NEOADJUVANT_TRASTUZUMAB_CREATE_ERROR")}, 500

        return patient_inclusion_criteria_neoadjuvant_trastuzumab.json(), 201


class PatientInclusionCriteriaNeoadjuvantTrastuzumabSearch(Resource):

    @jwt_required()
    @check('patient_inclusion_criteria_neoadjuvant_trastuzumab_search')
    @swag_from('../swagger/patient_inclusion_criteria_neoadjuvant_trastuzumab/search_patient_inclusion_criteria_neoadjuvant_trastuzumab.yaml')
    def post(self):
        query = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.patient_id == x)
            query = restrict(query, filters, 'diagnosed_invasive_adenocarcinoma', lambda x: x)
            query = restrict(query, filters, 'neoadjuvant_trastuzumab_her2_positive', lambda x: x)
            query = restrict(query, filters, 'determination_hormone_receptors', lambda x: x)
            query = restrict(query, filters, 'tumor_eq_ge_2cm', lambda x: x)
            query = restrict(query, filters, 'positive_axilla', lambda x: x)
            query = restrict(query, filters, 'marked_tumor_bed', lambda x: x)
            query = restrict(query, filters, 'blood_count_renal_hepatic_appropriate', lambda x: x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.user_modify.contains(x))
            query = restrict(query, filters, 'tumor_size_diameter_determined_by', lambda x: x)
            query = restrict(query, filters, 'positive_armpit_determined_by', lambda x: x)

        return paginated_results(query)
