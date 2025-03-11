import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.patient_inclusion_criteria import PatientInclusionCriteriaModel
from models.patient_inclusion_criteria_adjuvant_trastuzumab import PatientInclusionCriteriaAdjuvantTrastuzumabModel
from models.patient_inclusion_criteria_neoadjuvant_trastuzumab import \
    PatientInclusionCriteriaNeoadjuvantTrastuzumabModel
from resources.patient import patient_update_state
from security import check
from utils import restrict, paginated_results

class PatientInclusionCriteria(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('treatment_type', type=str)
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('specialty_id', type=int)
    parser.add_argument('patient_inclusion_criteria_adjuvant_id', type=int)
    parser.add_argument('patient_inclusion_criteria_neoadjuvant_id', type=int)
    parser.add_argument('has_signed_informed_consent', type=bool)
    parser.add_argument('patient_received_document', type=bool)
    parser.add_argument('consent_obtained_through_dialogue', type=bool)
    parser.add_argument('has_received_sufficient_sufficient', type=bool)
    parser.add_argument('has_asked_questions_and_can_continue_asking', type=bool)
    parser.add_argument('informed_receive_permanent_continuous_information', type=bool)
    parser.add_argument('information_received_clear_complete', type=bool)
    parser.add_argument('received_information_understandable_language', type=bool)
    parser.add_argument('treatment_hospital_id', type=int)
    parser.add_argument('patient_inclusion_criteria_adjuvant', type=dict, location='json')
    parser.add_argument('patient_inclusion_criteria_neoadjuvant', type=dict, location='json')
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('hospital_id', type=int)

    @jwt_required()
    @check('patient_inclusion_criteria_get')
    @swag_from('../swagger/patient_inclusion_criteria/get_patient_inclusion_criteria.yaml')
    def get(self, id):
        patient_inclusion_criteria = PatientInclusionCriteriaModel.find_by_id(id)
        if patient_inclusion_criteria:
            return patient_inclusion_criteria.json()
        return {'message': _("PATIENT_INCLUSION_CRITERIA_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_inclusion_criteria_update')
    @swag_from('../swagger/patient_inclusion_criteria/put_patient_inclusion_criteria.yaml')
    def put(self, id):
        patient_inclusion_criteria: PatientInclusionCriteriaModel = PatientInclusionCriteriaModel.find_by_id(id)
        if not patient_inclusion_criteria:
            return {'message': _("PATIENT_INCLUSION_CRITERIA_NOT_FOUND")}, 404

        # Requerimiento, RESTRINGIR EDICION DE FORMULARIOS DE INCLUSION Y EXCLUSION 24 HORAS DESPUES.
        try:
            difference = datetime.now() - patient_inclusion_criteria.date_create
            if difference.days >= 1:
                return {'message': _("PATIENT_INCLUSION_CRITERIA_UPDATE_24")}, 400
        except Exception as error:
            logging.error(f"An error occurred while calculating the difference between the inclusion form creation date. "
                          f"Detail:: {error.__cause__}")

        newdata = PatientInclusionCriteria.parser.parse_args()
        try:
            if newdata['treatment_type'] == 'adyuvante':
                patient_inclusion_adjuvant = newdata['patient_inclusion_criteria_adjuvant']
                # Ajuste de Prod
                if patient_inclusion_adjuvant.get('date_create', None):
                    del patient_inclusion_adjuvant['date_create']
                # Si no existe el modelo se crea
                patient_inclusion_adj_model = PatientInclusionCriteriaAdjuvantTrastuzumabModel()
                if 'id' in patient_inclusion_adjuvant and patient_inclusion_adjuvant['id']:
                    patient_inclusion_adj_model = PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(patient_inclusion_adjuvant['id'])
                PatientInclusionCriteriaAdjuvantTrastuzumabModel.from_reqparse(patient_inclusion_adj_model, patient_inclusion_adjuvant)
                patient_inclusion_adj_model.save_to_db()
                # Se asigna el id correspondiente a la cabecera
                newdata['patient_inclusion_criteria_adjuvant_id'] = patient_inclusion_adj_model.id
            elif newdata['treatment_type'] == 'neoadyuvante':
                patient_inclusion_neoadjuvant = newdata['patient_inclusion_criteria_neoadjuvant']
                # Ajuste de Prod
                if patient_inclusion_neoadjuvant.get('date_create', None):
                    del patient_inclusion_neoadjuvant['date_create']
                # Si no existe el modelo se crea
                patient_inclusion_neoadj_model = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel()
                if 'id' in patient_inclusion_neoadjuvant and patient_inclusion_neoadjuvant['id']:
                    patient_inclusion_neoadj_model = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(patient_inclusion_neoadjuvant['id'])
                PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.from_reqparse(patient_inclusion_neoadj_model, patient_inclusion_neoadjuvant)
                patient_inclusion_neoadj_model.save_to_db()
                # Se asigna el id correspondiente a la cabecera
                newdata['patient_inclusion_criteria_neoadjuvant_id'] = patient_inclusion_neoadj_model.id

            # Se elimina relacion redundante de la cabecera
            del newdata['patient_inclusion_criteria_adjuvant']
            del newdata['patient_inclusion_criteria_neoadjuvant']

            PatientInclusionCriteriaModel.from_reqparse(patient_inclusion_criteria, newdata)

            # Ajuste
            id_to_delete = None
            if newdata['treatment_type'] == 'adyuvante':
                if patient_inclusion_criteria.patient_inclusion_criteria_neoadjuvant_id:
                    id_to_delete = patient_inclusion_criteria.patient_inclusion_criteria_neoadjuvant_id
                    patient_inclusion_criteria.patient_inclusion_criteria_neoadjuvant_id = None
            elif newdata['treatment_type'] == 'neoadyuvante':
                if patient_inclusion_criteria.patient_inclusion_criteria_adjuvant_id:
                    id_to_delete = patient_inclusion_criteria.patient_inclusion_criteria_adjuvant_id
                    patient_inclusion_criteria.patient_inclusion_criteria_adjuvant_id = None

            # Persisitir
            patient_inclusion_criteria.user_modify = get_jwt_identity()
            patient_inclusion_criteria.date_modify = datetime.now()
            patient_inclusion_criteria.save_to_db()

            # Se borra eistencia del otro form, si corresponde
            if id_to_delete:
                if newdata['treatment_type'] == 'adyuvante':
                    patient_inclusion_neoadj_model = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(id_to_delete)
                    patient_inclusion_neoadj_model.delete_from_db()
                elif newdata['treatment_type'] == 'neoadyuvante':
                    patient_inclusion_adj_model = PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(id_to_delete)
                    patient_inclusion_adj_model.delete_from_db()

        except Exception as error:
            logging.error('An error occurred while modifying Patient Inclusion Criteria.', exc_info=error)
            return {"message": _("PATIENT_INCLUSION_CRITERIA_UPDATE_ERROR")}, 500

        # LLamar evento de cambio de estado de paciente
        patient_update_state(newdata.get('patient_id', None))

        return patient_inclusion_criteria.json(1)


    @jwt_required()
    @check('patient_inclusion_criteria_delete')
    @swag_from('../swagger/patient_inclusion_criteria/delete_patient_inclusion_criteria.yaml')
    def delete(self, id):
        patient_inclusion_criteria = PatientInclusionCriteriaModel.find_by_id(id)
        if patient_inclusion_criteria:
            patient_inclusion_criteria.delete_from_db()

        return {'message': _("PATIENT_INCLUSION_CRITERIA_DELETED")}


class PatientInclusionCriteriaList(Resource):

    @jwt_required()
    @check('patient_inclusion_criteria_list')
    @swag_from('../swagger/patient_inclusion_criteria/list_patient_inclusion_criteria.yaml')
    def get(self):
        query = PatientInclusionCriteriaModel.query
        return paginated_results(query)

    @jwt_required()
    @check('patient_inclusion_criteria_insert')
    @swag_from('../swagger/patient_inclusion_criteria/post_patient_inclusion_criteria.yaml')
    def post(self):
        data = PatientInclusionCriteria.parser.parse_args()

        id = data.get('id')

        if id is not None and PatientInclusionCriteriaModel.find_by_id(id):
            return {'message': _("PATIENT_INCLUSION_CRITERIA_DUPLICATED").format(id)}, 400
        try:
            # se debe recuperar los datos de patient_inclusion_criteria_adjuvant o neoadjuvant
            if data['treatment_type'] == 'adyuvante':
                patient_inclusion_adjuvant = data['patient_inclusion_criteria_adjuvant']
                patient_inclusion_adjuvant_model = PatientInclusionCriteriaAdjuvantTrastuzumabModel(**patient_inclusion_adjuvant)
                patient_inclusion_adjuvant_model.save_to_db()
                data['patient_inclusion_criteria_adjuvant_id'] = patient_inclusion_adjuvant_model.id
            elif data['treatment_type'] == 'neoadyuvante':
                patient_inclusion_neoadjuvant = data['patient_inclusion_criteria_neoadjuvant']
                patient_inclusion_neoadjuvant_model = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel(**patient_inclusion_neoadjuvant)
                patient_inclusion_neoadjuvant_model.save_to_db()
                data['patient_inclusion_criteria_neoadjuvant_id'] = patient_inclusion_neoadjuvant_model.id
            del data['patient_inclusion_criteria_adjuvant']
            del data['patient_inclusion_criteria_neoadjuvant']
            patient_inclusion_criteria = PatientInclusionCriteriaModel(**data)

            patient_inclusion_criteria.user_create = get_jwt_identity()
            patient_inclusion_criteria.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating Patient Inclusion Criteria.', exc_info=e)
            return {"message": _("PATIENT_INCLUSION_CRITERIA_CREATE_ERROR")}, 500

        # LLamar evento de cambio de estado de paciente
        patient_update_state(data.get('patient_id', None))

        return patient_inclusion_criteria.json(1), 201


class PatientInclusionCriteriaSearch(Resource):

    @jwt_required()
    @check('patient_inclusion_criteria_search')
    @swag_from('../swagger/patient_inclusion_criteria/search_patient_inclusion_criteria.yaml')
    def post(self):
        query = PatientInclusionCriteriaModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PatientInclusionCriteriaModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: PatientInclusionCriteriaModel.patient_id == x)
            query = restrict(query, filters, 'treatment_type', lambda x: PatientInclusionCriteriaModel.treatment_type.contains(x))
            query = restrict(query, filters, 'doctor_id', lambda x: PatientInclusionCriteriaModel.treatment_type.contains(x))
            query = restrict(query, filters, 'specialty_id', lambda x: PatientInclusionCriteriaModel.treatment_type.contains(x))
            query = restrict(query, filters, 'patient_inclusion_criteria_adjuvant_id', lambda x: PatientInclusionCriteriaModel.patient_inclusion_criteria_adjuvant_id == x)
            query = restrict(query, filters, 'patient_inclusion_criteria_neoadjuvant_id', lambda x: PatientInclusionCriteriaModel.patient_inclusion_criteria_neoadjuvant_id == x)
            query = restrict(query, filters, 'has_signed_informed_consent', lambda x: x)
            query = restrict(query, filters, 'patient_received_document', lambda x: x)
            query = restrict(query, filters, 'consent_obtained_through_dialogue', lambda x: x)
            query = restrict(query, filters, 'has_received_sufficient_sufficient', lambda x: x)
            query = restrict(query, filters, 'has_asked_questions_and_can_continue_asking', lambda x: x)
            query = restrict(query, filters, 'informed_receive_permanent_continuous_information', lambda x: x)
            query = restrict(query, filters, 'information_received_clear_complete', lambda x: x)
            query = restrict(query, filters, 'received_information_understandable_language', lambda x: x)
            query = restrict(query, filters, 'treatment_hospital_id', lambda x: PatientInclusionCriteriaModel.treatment_hospital_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(PatientInclusionCriteriaModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: PatientInclusionCriteriaModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(PatientInclusionCriteriaModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: PatientInclusionCriteriaModel.user_modify.contains(x))
            query = restrict(query, filters, 'hospital_id', lambda x: PatientInclusionCriteriaModel.hospital_id == x)

        return paginated_results(query)
