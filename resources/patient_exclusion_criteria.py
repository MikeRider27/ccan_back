import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.patient_exclusion_criteria import PatientExclusionCriteriaModel
from resources.patient import patient_update_state
from security import check
from utils import restrict, paginated_results


class PatientExclusionCriteria(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('distant_metastatic', type=bool)
    parser.add_argument('life_expectancy_greater_5_comorbidities', type=bool)
    parser.add_argument('fevi_less_50', type=bool)
    parser.add_argument('ecog_eq_greater_2', type=bool)
    parser.add_argument('congestive_ic', type=bool)
    parser.add_argument('ischemic_heart_disease', type=bool)
    parser.add_argument('arritmia_inestable', type=bool)
    parser.add_argument('valve_disease', type=bool)
    parser.add_argument('uncontrolled_hta', type=bool)
    parser.add_argument('doxorubicin_greater_360mg_by_m2', type=bool)
    parser.add_argument('epirrubicina_greater_720mg_by_m2', type=bool)
    parser.add_argument('pregnancy', type=bool)
    parser.add_argument('lactation', type=bool)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('hospital_id', type=int)

    @jwt_required()
    @check('patient_exclusion_criteria_get')
    @swag_from('../swagger/patient_exclusion_criteria/get_patient_exclusion_criteria.yaml')
    def get(self, id):
        patient_exclusion_criteria = PatientExclusionCriteriaModel.find_by_id(id)
        if patient_exclusion_criteria:
            return patient_exclusion_criteria.json()
        return {'message': _("PATIENT_EXCLUSION_CRITERIA_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_exclusion_criteria_update')
    @swag_from('../swagger/patient_exclusion_criteria/put_patient_exclusion_criteria.yaml')
    def put(self, id):
        patient_exclusion_criteria: PatientExclusionCriteriaModel = PatientExclusionCriteriaModel.find_by_id(id)
        if patient_exclusion_criteria:
            # Requerimiento, RESTRINGIR EDICION DE FORMULARIOS DE INCLUSION Y EXCLUSION 24 HORAS DESPUES.
            try:
                difference = datetime.now() - patient_exclusion_criteria.date_create
                if difference.days >= 1:
                    return {'message': _("PATIENT_EXCLUSION_CRITERIA_UPDATE_24")}, 400
            except Exception as error:
                logging.error(
                    f"An error occurred while calculating the difference between the inclusion form creation date. "
                    f"Details: {error.__cause__}")

            newdata = PatientExclusionCriteria.parser.parse_args()
            PatientExclusionCriteriaModel.from_reqparse(patient_exclusion_criteria, newdata)

            patient_exclusion_criteria.user_modify = get_jwt_identity()
            patient_exclusion_criteria.date_modify = datetime.now()
            patient_exclusion_criteria.save_to_db()

            # LLamar evento de cambio de estado de paciente
            patient_update_state(newdata.get('patient_id', None))

            return patient_exclusion_criteria.json()

        return {'message': _("PATIENT_EXCLUSION_CRITERIA_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_exclusion_criteria_delete')
    @swag_from('../swagger/patient_exclusion_criteria/delete_patient_exclusion_criteria.yaml')
    def delete(self, id):
        patient_exclusion_criteria = PatientExclusionCriteriaModel.find_by_id(id)
        if patient_exclusion_criteria:
            patient_exclusion_criteria.delete_from_db()

        return {'message': _("PATIENT_EXCLUSION_CRITERIA_DELETED")}


class PatientExclusionCriteriaList(Resource):

    @jwt_required()
    @check('patient_exclusion_criteria_list')
    @swag_from('../swagger/patient_exclusion_criteria/list_patient_exclusion_criteria.yaml')
    def get(self):
        query = PatientExclusionCriteriaModel.query
        return paginated_results(query)

    @jwt_required()
    @check('patient_exclusion_criteria_insert')
    @swag_from('../swagger/patient_exclusion_criteria/post_patient_exclusion_criteria.yaml')
    def post(self):
        data = PatientExclusionCriteria.parser.parse_args()

        id = data.get('id')

        if id is not None and PatientExclusionCriteriaModel.find_by_id(id):
            return {'message': _("PATIENT_EXCLUSION_CRITERIA_DUPLICATED").format(id)}, 400

        patient_exclusion_criteria = PatientExclusionCriteriaModel(**data)
        try:
            patient_exclusion_criteria.user_create = get_jwt_identity()
            patient_exclusion_criteria.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating patient_exclusion_criteria.', exc_info=e)
            return {"message": _("PATIENT_EXCLUSION_CRITERIA_CREATE_ERROR")}, 500

        # LLamar evento de cambio de estado de paciente
        patient_update_state(data.get('patient_id', None))

        return patient_exclusion_criteria.json(), 201


class PatientExclusionCriteriaSearch(Resource):

    @jwt_required()
    @check('patient_exclusion_criteria_search')
    @swag_from('../swagger/patient_exclusion_criteria/search_patient_exclusion_criteria.yaml')
    def post(self):
        query = PatientExclusionCriteriaModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PatientExclusionCriteriaModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: PatientExclusionCriteriaModel.patient_id == x)
            query = restrict(query, filters, 'distant_metastatic', lambda x: x)
            query = restrict(query, filters, 'life_expectancy_greater_5_comorbidities', lambda x: x)
            query = restrict(query, filters, 'fevi_less_50', lambda x: x)
            query = restrict(query, filters, 'ecog_eq_greater_2', lambda x: x)
            query = restrict(query, filters, 'congestive_ic', lambda x: x)
            query = restrict(query, filters, 'ischemic_heart_disease', lambda x: x)
            query = restrict(query, filters, 'arritmia_inestable', lambda x: x)
            query = restrict(query, filters, 'valve_disease', lambda x: x)
            query = restrict(query, filters, 'uncontrolled_hta', lambda x: x)
            query = restrict(query, filters, 'doxorubicin_greater_360mg_by_m2', lambda x: x)
            query = restrict(query, filters, 'epirrubicina_greater_720mg_by_m2', lambda x: x)
            query = restrict(query, filters, 'pregnancy', lambda x: x)
            query = restrict(query, filters, 'lactation', lambda x: x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(PatientExclusionCriteriaModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: PatientExclusionCriteriaModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(PatientExclusionCriteriaModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: PatientExclusionCriteriaModel.user_modify.contains(x))
            query = restrict(query, filters, 'hospital_id', lambda x: PatientExclusionCriteriaModel.hospital_id == x)
        return paginated_results(query)
