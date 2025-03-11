import csv
import logging
from datetime import datetime
from enum import Enum
from io import BytesIO, StringIO

import pandas as pd
import requests
from flasgger import swag_from
from flask import request, current_app, send_file, make_response
from flask_babel import _
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import aliased

from dao.medical_documents_dao import MedicalDocumentsDao
from dao.patient_dao import PatientDao
from db import db
from models.area import AreaModel
from models.breast_form import BreastFormModel
from models.cervix_form import CervixFormModel
from models.chemotherapy import ChemotherapyModel
from models.chemotherapy_treatment_plan import ChemotherapyTreatmentPlanModel
from models.cie_10 import Cie_10Model
from models.cie_o_morphology import CieOMorphologyModel
from models.cie_o_topography import CieOTopographyModel
from models.cie_o_tumor_location import CieOTumorLocationModel
from models.city import CityModel
from models.committee import CommitteeModel
from models.country import CountryModel
from models.destinatarios import DestinatariosModel
from models.diagnosis import DiagnosisModel
from models.diagnosis_ap import DiagnosisApModel
from models.dispatch_medications import DispatchMedicationsModel
from models.document_type import DocumentTypeModel
from models.evaluation import EvaluationModel
from models.follow_up_treatment_plan import FollowUpTreatmentPlanModel
from models.gender import GenderModel
from models.hospital import HospitalModel
from models.medical_committee import MedicalCommitteeModel
from models.medical_consultation import MedicalConsultationModel
from models.medical_document import MedicalDocumentModel
from models.message import MessageModel
from models.notificaciones import NotificacionesModel
from models.parameter import ParameterModel
from models.patient import PatientModel, OriginsCode
from models.patient_exclusion_criteria import PatientExclusionCriteriaModel
from models.patient_hospital import PatientHospitalModel
from models.patient_inclusion_criteria import PatientInclusionCriteriaModel
from models.patient_inclusion_criteria_adjuvant_trastuzumab import PatientInclusionCriteriaAdjuvantTrastuzumabModel
from models.patient_inclusion_criteria_neoadjuvant_trastuzumab import \
    PatientInclusionCriteriaNeoadjuvantTrastuzumabModel
from models.personal_pathological_history import PersonalPathologicalHistoryModel
from models.radiotherapy import RadiotherapyModel
from models.surgery import SurgeryModel
from models.treatment_follow_up import TreatmentFollowUpModel
from models.treatment_plan import TreatmentPlanModel
from models.user import UserModel
from security import check
from utils import paginated_results, restrict_collector, sorting_relationship_type, parse_date


class Patient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('firstname', type=str)
    parser.add_argument('lastname', type=str)
    parser.add_argument('document_number', type=str)
    parser.add_argument('state_id', type=int)
    parser.add_argument('vital_state_id', type=int)
    parser.add_argument('birthdate', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('address', type=str)
    parser.add_argument('gender_id', type=int)
    parser.add_argument('document_type_id', type=int)
    parser.add_argument('country_id', type=int)
    parser.add_argument('area_id', type=int)
    parser.add_argument('city_id', type=int)
    parser.add_argument('nationality_id', type=int)
    parser.add_argument('phone', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('registration_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('civil_status_id', type=int)
    parser.add_argument('responsible_firstname', type=str)
    parser.add_argument('responsible_lastname', type=str)
    parser.add_argument('responsible_relationship', type=str)
    parser.add_argument('responsible_phone', type=str)
    parser.add_argument('number_card', type=int)
    parser.add_argument('origin', type=str)
    parser.add_argument('hospital_list', type=list, location='json')

    @jwt_required()
    @check('patient_get')
    @swag_from('../swagger/patient/get_patient.yaml')
    def get(self, id):
        patient = PatientModel.find_by_id(id)
        if patient:
            return patient.json(4)
        return {'message': _("PATIENT_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_update')
    @swag_from('../swagger/patient/put_patient.yaml')
    def put(self, id):
        patient = PatientModel.find_by_id(id)
        if patient:
            newdata = Patient.parser.parse_args()
            patient_hospital_data_list = newdata['hospital_list']
            PatientModel.from_reqparse(patient, newdata)

            # hospital_list update
            patient_hospital_list = []
            for patient_hospital_data in patient_hospital_data_list:
                if patient_hospital_data.get('id', None):
                    patient_hospital_model = PatientHospitalModel.find_by_id(patient_hospital_data['id'])
                    PatientHospitalModel.from_reqparse(patient_hospital_model, patient_hospital_data)
                else:
                    patient_hospital_model = PatientHospitalModel(**patient_hospital_data)
                patient_hospital_list.append(patient_hospital_model)

            patient.hospital_list = patient_hospital_list

            patient.user_modify = get_jwt_identity()
            patient.date_modify = datetime.now()
            patient.save_to_db()
            return patient.json(4)
        return {'message': _("PATIENT_NOT_FOUND")}, 404

    @jwt_required()
    @check('patient_delete')
    @swag_from('../swagger/patient/delete_patient.yaml')
    def delete(self, id):
        # Get user Admin
        username = get_jwt_identity()
        user: UserModel = UserModel.query.filter_by(user=username).first()
        if not user or (user and not user.administrator):
            return {'message': _("NO_PERMISSION")}, 403

        patient = PatientModel.find_by_id(id)
        if not patient:
            return {'message': _("PATIENT_NOT_FOUND")}, 404

        try:
            with db.session.no_autoflush:
                diagnosis_list = DiagnosisModel.query.filter_by(patient_id=patient.id)
                if diagnosis_list:
                    for diagnosis in diagnosis_list:
                        db.session.delete(diagnosis)

                treatment_plan_list = TreatmentPlanModel.query.filter_by(patient_id=patient.id).all()
                if treatment_plan_list:
                    for treatment_plan in treatment_plan_list:
                        follow_up_treatment_plan_list = FollowUpTreatmentPlanModel.query.filter_by(
                            treatment_plan_id=treatment_plan.id).all()
                        if follow_up_treatment_plan_list:
                            for follow_up_treatment_plan in follow_up_treatment_plan_list:
                                db.session.delete(follow_up_treatment_plan)

                        chemotherapy_treatment_plan_list = ChemotherapyTreatmentPlanModel.query.filter_by(
                            treatment_plan_id=treatment_plan.id).all()
                        if chemotherapy_treatment_plan_list:
                            for chemotherapy_treatment_plan in chemotherapy_treatment_plan_list:
                                db.session.delete(chemotherapy_treatment_plan)

                        db.session.delete(treatment_plan)

                follow_up_list = TreatmentFollowUpModel.query.filter_by(patient_id=patient.id)
                if follow_up_list:
                    for follow_up in follow_up_list:
                        db.session.delete(follow_up)

                diagnosis_ap_list = DiagnosisApModel.query.filter_by(patient_id=patient.id)
                if diagnosis_ap_list:
                    for diagnosis_ap in diagnosis_ap_list:
                        db.session.delete(diagnosis_ap)

                medical_document_list = MedicalDocumentModel.query.filter_by(patient_id=patient.id)
                if medical_document_list:
                    for medical_document in medical_document_list:
                        db.session.delete(medical_document)

                evaluation_list = EvaluationModel.query.filter_by(patient_id=patient.id)
                if evaluation_list:
                    for evaluation in evaluation_list:
                        db.session.delete(evaluation)

                medical_consultation_list = MedicalConsultationModel.query.filter_by(patient_id=patient.id)
                if medical_consultation_list:
                    for medical_consultation in medical_consultation_list:
                        db.session.delete(medical_consultation)

                patient_exclusion_criteria_list = PatientExclusionCriteriaModel.query.filter_by(patient_id=patient.id)
                if patient_exclusion_criteria_list:
                    for patient_exclusion_criteria in patient_exclusion_criteria_list:
                        db.session.delete(patient_exclusion_criteria)

                patient_inclusion_criteria_list = PatientInclusionCriteriaModel.query.filter_by(patient_id=patient.id)
                if patient_inclusion_criteria_list:
                    for patient_inclusion_criteria in patient_inclusion_criteria_list:
                        db.session.delete(patient_inclusion_criteria)

                patient_inclusion_criteria_adjuvant_trastuzumab_list = PatientInclusionCriteriaAdjuvantTrastuzumabModel.query.filter_by(
                    patient_id=patient.id)
                if patient_inclusion_criteria_adjuvant_trastuzumab_list:
                    for patient_inclusion_criteria_adjuvant_trastuzumab in patient_inclusion_criteria_adjuvant_trastuzumab_list:
                        db.session.delete(patient_inclusion_criteria_adjuvant_trastuzumab)

                patient_inclusion_criteria_neoadjuvant_trastuzumab_list = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.query.filter_by(
                    patient_id=patient.id)
                if patient_inclusion_criteria_neoadjuvant_trastuzumab_list:
                    for patient_inclusion_criteria_neoadjuvant_trastuzumab in patient_inclusion_criteria_neoadjuvant_trastuzumab_list:
                        db.session.delete(patient_inclusion_criteria_neoadjuvant_trastuzumab)

                personal_pathological_history_list = PersonalPathologicalHistoryModel.query.filter_by(
                    patient_id=patient.id)
                if personal_pathological_history_list:
                    for personal_pathological_history in personal_pathological_history_list:
                        db.session.delete(personal_pathological_history)

                chemotherapy_list = ChemotherapyModel.query.filter_by(patient_id=patient.id)
                if chemotherapy_list:
                    for chemotherapy in chemotherapy_list:
                        db.session.delete(chemotherapy)

                radiotherapy_list = RadiotherapyModel.query.filter_by(patient_id=patient.id)
                if radiotherapy_list:
                    for radiotherapy in radiotherapy_list:
                        db.session.delete(radiotherapy)

                surgery_list = SurgeryModel.query.filter_by(patient_id=patient.id)
                if surgery_list:
                    for surgery in surgery_list:
                        db.session.delete(surgery)

                committee_list = CommitteeModel.query.filter_by(patient_id=patient.id)
                if committee_list:
                    for committee in committee_list:
                        medical_committee_list = MedicalCommitteeModel.query.filter_by(committee_id=committee.id)
                        if medical_committee_list:
                            for medical_committee in medical_committee_list:
                                db.session.delete(medical_committee)

                        db.session.delete(committee)

                cervix_form_list = CervixFormModel.query.filter_by(patient_id=patient.id)
                if cervix_form_list:
                    for cervix_form in cervix_form_list:
                        db.session.delete(cervix_form)

                breast_form_list = BreastFormModel.query.filter_by(patient_id=patient.id)
                if breast_form_list:
                    for breast_form in breast_form_list:
                        db.session.delete(breast_form)

                message_list = MessageModel.query.filter_by(patient_id=patient.id)
                if message_list:
                    for message in message_list:
                        destinatario_list = DestinatariosModel.query.filter_by(message_id=message.id)
                        if destinatario_list:
                            for destinatario in destinatario_list:
                                db.session.delete(destinatario)

                        notificationes_list = NotificacionesModel.query.filter_by(message_id=message.id)
                        if notificationes_list:
                            for notificationes in notificationes_list:
                                db.session.delete(notificationes)

                        db.session.delete(message)

                db.session.delete(patient)
                db.session.commit()
        except Exception as error:
            # Se revierte los cambios
            db.session.rollback()
            logging.error(_("PATIENT_DELETE_ERROR"), exc_info=error)
            return {"message": _("PATIENT_DELETE_ERROR")}, 500

        return {'message': _("PATIENT_DELETED")}


class PatientList(Resource):

    @jwt_required()
    @check('patient_list')
    @swag_from('../swagger/patient/list_patient.yaml')
    def get(self):
        query = PatientModel.query
        return paginated_results(query, is_patient=True)

    @jwt_required()
    @check('patient_insert')
    @swag_from('../swagger/patient/post_patient.yaml')
    def post(self):
        data = Patient.parser.parse_args()

        # Validaciones de Duplicidad
        id = data.get('id')
        if id is not None and PatientModel.find_by_id(id):
            return {'message': _("PATIENT_DUPLICATED").format(id)}, 400

        cipher_key = current_app.config['ENCRYPTION_KEY']
        document_number = data.get('document_number')
        patient_model = PatientModel.query.filter(
            func.decrypt_data(PatientModel.document_number, cipher_key) == document_number).first()
        if patient_model:
            return {'message': "Ya existe un paciente con Número de Documento: {}.".format(document_number)}, 400

        patient_hospital_data_list = data['hospital_list']
        del data['hospital_list']

        patient = PatientModel(**data)

        # hospital_list
        for patient_hospital_data in patient_hospital_data_list:
            patient_hospital_model = PatientHospitalModel(**patient_hospital_data)
            patient.hospital_list.append(patient_hospital_model)

        try:
            patient.user_create = get_jwt_identity()
            patient.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating Patient.', exc_info=e)
            return {"message": _("PATIENT_CREATE_ERROR")}, 500

        return patient.json(), 201


class PatientSearchNative(Resource):

    @jwt_required()
    @check('patient_search')
    @swag_from('../swagger/patient/search_patient.yaml')
    def post(self):
        patient_dao = PatientDao()
        filters = {}

        if request.json:
            filters = request.json

        patient_paginated = patient_dao.get_patient_paginated(filters)

        return patient_paginated, 200


class PatientSearch(Resource):

    @jwt_required()
    @check('patient_search')
    @swag_from('../swagger/patient/search_patient.yaml')
    def post(self):
        key = current_app.config['ENCRYPTION_KEY']
        query = PatientModel.query
        hospital_id = request.json.get('hospital_id')

        # Relationship
        state = aliased(ParameterModel)
        query = query.join(state, and_(PatientModel.state_id == state.id,
                                       state.domain == 'PATIENT_STATE'), isouter=True)
        document_type = aliased(DocumentTypeModel)
        query = query.join(document_type, PatientModel.document_type_id == document_type.id, isouter=True)
        gender = aliased(GenderModel)
        query = query.join(gender, PatientModel.gender_id == gender.id, isouter=True)

        #Joins para origins
        query = query \
            .outerjoin(DispatchMedicationsModel, PatientModel.id == DispatchMedicationsModel.patient_id) \
            .outerjoin(MedicalConsultationModel, PatientModel.id == MedicalConsultationModel.patient_id) \
            .group_by(PatientModel.id)

        # Join condicional por filtro debido a duplicacion por tabla intermedia
        if hospital_id:
            patient_hospital = aliased(PatientHospitalModel)
            query = query.join(patient_hospital, PatientModel.id == patient_hospital.patient_id, isouter=True)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            # filter_list = restrict_collector(filter_list, filters, 'id', lambda x: PatientModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'firstname', lambda x: func.lower(
                func.decrypt_data(PatientModel.firstname, key)).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'lastname', lambda x: func.lower(
                func.decrypt_data(PatientModel.lastname, key)).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'document_number', lambda x: func.lower(
                func.decrypt_data(PatientModel.document_number, key)).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'birthdate',
                                                lambda x: func.to_char(PatientModel.birthdate, 'DD/MM/YYYY').contains(
                                                    x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_create',
                                                lambda x: func.to_char(PatientModel.date_create, 'DD/MM/YYYY').contains(
                                                    x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_create',
                                                lambda x: PatientModel.user_create.contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_modify',
                                                lambda x: func.to_char(PatientModel.date_modify, 'DD/MM/YYYY').contains(
                                                    x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_modify',
                                                lambda x: PatientModel.user_modify.contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'registration_date',
                                                lambda x: func.to_char(PatientModel.registration_date,
                                                                       'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'origins',
                                                lambda x: or_(
                                                    func.lower(PatientModel.origin).contains(func.lower(x)),
                                                    func.lower(DispatchMedicationsModel.origin).contains(
                                                        func.lower(x)),
                                                    func.lower(MedicalConsultationModel.origin).contains(
                                                        func.lower(x))
                                                ))
            # Relationship Filter
            # Join condicional por filtro
            if hospital_id:
                and_filter_list = restrict_collector(and_filter_list, filters, 'hospital_id',
                                                     lambda x: patient_hospital.hospital_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'state',
                                                lambda x: func.lower(state.value).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'document_type',
                                                lambda x: func.lower(document_type.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'gender',
                                                lambda x: func.lower(gender.description).contains(func.lower(x)))

            # Apply filters
            general_filter = request.args.get('general_filter', None, str) == 'true'
            if general_filter:
                query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
            else:
                filter_list = and_filter_list + or_filter_list
                query = query.filter(and_(*filter_list))

        # Capture Relationship Sorting and configure performance
        sort = True
        sort_by = request.args.get('sortBy', None, str)
        if sort_by:
            if sort_by == 'state':
                query = sorting_relationship_type(request, query, state.value)
                sort = False
            elif sort_by == 'document_type':
                query = sorting_relationship_type(request, query, document_type.description)
                sort = False
            elif sort_by == 'gender':
                query = sorting_relationship_type(request, query, gender.description)
                sort = False

        return paginated_results(query, sort, is_patient=True)


class ServicePatient(Resource):
    @jwt_required()
    @check('patient_service_cedula')
    @swag_from('../swagger/patient/get_patient_cedula.yaml')
    def get(self, ciPatient):
        username = current_app.config['AUTH_MSPBS_USER']
        password = current_app.config['AUTH_MSPBS_PASS']
        url = current_app.config['BACKEND_MSPBS_URL']
        params = {
            'cedula': ciPatient
        }

        try:
            # Create a requests session and set the authentication credentials
            with requests.Session() as session:
                session.auth = (username, password)
                # Perform the GET request
                response = session.get(url, params=params, verify=False)
                # Check the response status code
                if response.status_code == 200:
                    try:
                        data = response.json()
                        data['fecha_nacimiento'] = self.change_date_format(data['fecha_nacimiento'])
                        data['codigo_genero'] = int(data['codigo_genero'])
                        return data  # Assuming the response is in JSON format
                    except requests.exceptions.RequestException as e:
                        return f"Error: {e}"
                elif response.status_code == 401:
                    return "Unauthorized: Invalid credentials"
                else:
                    return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def change_date_format(self, date_string):
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')

        # Format the datetime object back into 'dd-mm-yyyy' format
        return date_obj.strftime('%d-%m-%Y')

    def get_gender_name(gender):
        if gender == Gender.Femenino:
            return 1
        elif gender == Gender.Masculino:
            return 2
        else:
            return 3


class Gender(Enum):
    Femenino = 1
    Masculino = 2
    SD = 3


def patient_update_state(patient_id):
    """
    Metodo encargado de actualizar el estado del paciente
    :param patient_id:
    :return:
    """
    if not patient_id:
        return

    patient = PatientModel.query.filter_by(id=patient_id).first()
    if not patient:
        return

    actual_state = patient.state.code
    final_state = None

    # Si formulario de inclusion y exclusion completo => En Evaluacion
    if actual_state == 'SOSP':
        excluded = False
        doc_en_falta = []

        # Inclusion Criteria
        inclusion_form = False
        patientInclusionCriteriaModel = PatientInclusionCriteriaModel.query.filter_by(patient_id=patient_id).order_by(
            PatientInclusionCriteriaModel.date_create.desc()).first()
        if patientInclusionCriteriaModel:
            if patientInclusionCriteriaModel.patient_inclusion_criteria_adjuvant_id:
                id = patientInclusionCriteriaModel.patient_inclusion_criteria_adjuvant_id
                inclusion_form = PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(id)
                if not inclusion_form.patient_included():
                    # Excluir paciente
                    excluded = True
            elif patientInclusionCriteriaModel.patient_inclusion_criteria_neoadjuvant_id:
                id = patientInclusionCriteriaModel.patient_inclusion_criteria_neoadjuvant_id
                inclusion_form = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(id)
                if not inclusion_form.patient_included():
                    # Excluir paciente
                    excluded = True
                    doc_en_falta = inclusion_form.get_documentos_faltantes()

        # Exclusion criteria
        exclusion_form = PatientExclusionCriteriaModel.query.filter_by(patient_id=patient_id).order_by(
            PatientExclusionCriteriaModel.date_create.desc()).first()
        if exclusion_form:
            if exclusion_form.patient_excluded():
                # Excluir paciente
                excluded = True

        # Verificar que los documentos del checklist esten completados
        medical_documents_dao = MedicalDocumentsDao()
        type_list = medical_documents_dao.get_requirements_files_data(patient_id=patient_id)
        type_list = [doc for doc in type_list]
        checkListComplete = all(all(doc['id'] is not None for id in doc) for doc in type_list)

        # Si ambos formularios fueron completados
        if checkListComplete and len(doc_en_falta) == 0:
            if inclusion_form and exclusion_form:
                if excluded:
                    # Excluir paciente
                    # Se deshabilita excluksion de paciente por sistema
                    # final_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='EXCL').first()
                    pass
                else:
                    # Evaluar paciente
                    final_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='EVAL').first()

    # Resultado de la evaluacion
    if actual_state == 'EVAL' or actual_state == 'REV':
        eval_form = EvaluationModel.query.filter_by(patient_id=patient_id).order_by(
            EvaluationModel.id.desc()).first()
        if eval_form:
            if eval_form.evaluation_state == 'revision':
                # Paciente en revision
                final_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='REV').first()
            elif eval_form.evaluation_state == 'approved':
                # Incluir paciente
                final_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='INCL').first()
            elif eval_form.evaluation_state == 'excluded':
                # Excluir paciente
                final_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='EXCL').first()

    # Si tiene Plan de tratamiento activo => En tratamiento
    if actual_state == 'INCL' or actual_state == 'FIN':
        tp_state_in_progress = ParameterModel.query.filter_by(domain='TREATMENT_PLAN_STATE',
                                                              code='tret_pla_cur').first()
        treatment_plan_form = TreatmentPlanModel.query.filter_by(patient_id=patient_id,
                                                                 state_id=tp_state_in_progress.id).order_by(
            TreatmentPlanModel.date_create.desc()).first()
        if treatment_plan_form:
            # Paciente en tratamiento
            final_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='TREATMENT').first()

    # Si plan de tratamiento Finalizado, estado Finalizado
    # if actual_state == 'TREATMENT':
    #     tp_state_in_progress = ParameterModel.query.filter_by(domain='TREATMENT_PLAN_STATE', code='tret_pla_cur').first()
    #     treatment_plan_form_active = TreatmentPlanModel.query.filter_by(patient_id=patient_id, state_id=tp_state_in_progress.id).order_by(
    #         TreatmentPlanModel.date_create.desc()).first()
    #     treatment_plan_form_list = TreatmentPlanModel.query.filter_by(patient_id=patient_id).order_by(
    #         TreatmentPlanModel.date_create.desc()).all()
    #     if not treatment_plan_form_active and len(treatment_plan_form_list) > 0:
    #         # Tratamiento de Paciente finalizado
    #         final_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='FIN').first()

    # Esta Fallecido, se setea de forma manual

    # Se define el siguiente estado del paciente
    if final_state:
        patient.state_id = final_state.id
        patient.save_to_db(encrypt=False)


class PatientByDocument(Resource):
    @jwt_required()
    @check('patient_get')
    @swag_from('../swagger/patient/get_patient.yaml')
    def get(self, document):
        key = current_app.config['ENCRYPTION_KEY']
        patient = PatientModel.query.filter(func.decrypt_data(PatientModel.document_number, key) == document).first()
        if patient:
            return patient.json(1)
        return {'message': f'Patient with document number cannot be found {document}'}, 404


class PatientsAll(Resource):
    @jwt_required()
    @check('report_patient_csv_download')
    def get(self):
        patient_dao = PatientDao()
        patient_list = patient_dao.get_patients_all()

        if len(patient_list) == 0:
            return {'message': _("REPORT_DATA_NOT_FOUND")}, 404

        df = pd.json_normalize(patient_list)

        # Create an output stream for CSV
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Finally return the file as CSV
        return send_file(output, attachment_filename="patient_report.csv", as_attachment=True, mimetype='text/csv')


class PatientImport(Resource):
    REQUIRED_COLUMNS = [
        'nombre_establecimiento', 'tipo_documento', 'documento_nro', 'nombres', 'apellidos', 'sexo', 'fecha_nac', 'fecha_dx_ap', 'fecha_dx'
    ]

    @jwt_required()
    def get(self):
        """
        Método encargado de proveer el archivo de importación requerido para importar pacientes
        :return: archivo Excel con las columnas indicadas y múltiples hojas
        """
        # Definir las columnas necesarias
        columns = [
            'nombre_establecimiento', 'tipo_documento', 'documento_nro', 'nombres', 'apellidos', 'sexo',
            'fecha_nac', 'fecha_validacion', 'fecha_dx_ap', 'codigo_morfologia', 'clasificacion', 'cie10', 'fecha_dx',
            'complementario', 're', 'rp', 'her2', 'tamanho_tumor', 'cod_topografia', 'cod_localizacion', 'material',
            'dx_presuntivo', 'idsolicitud', 'macroscopia', 'microscopia', 'diagnostico', 'direccion', 'pais',
            'departamento', 'ciudad', 'telefono', 'nacionalidad', 'estadocivil', 'nro_ficha'
        ]

        # Valores opcionales o requeridos
        values = [
            'requerido', 'requerido', 'requerido', 'requerido', 'requerido', 'requerido', 'requerido', 'opcional',
            'requerido', 'opcional', 'opcional', 'opcional', 'requerido', 'opcional', 'opcional', 'opcional',
            'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional',
            'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional', 'opcional'
        ]

        # Crear un DataFrame vacío con las columnas
        df_pacientes = pd.DataFrame([values], columns=columns)

        # Especificación de valores
        # nombre_establecimiento
        columns = ['nombre_establecimiento']
        values = list(map(lambda x: x.description, HospitalModel.query.all()))
        df_nombre_establecimiento = pd.DataFrame(values, columns=columns)

        # tipo_documento
        columns = ['tipo_documento']
        values = list(map(lambda x: x.code, DocumentTypeModel.query.all()))
        df_tipo_documento = pd.DataFrame(values, columns=columns)

        # sexo
        columns = ['sexo']
        values = list(map(lambda x: x.code, GenderModel.query.all()))
        df_sexo = pd.DataFrame(values, columns=columns)

        # cie10
        columns = ['cie10']
        values = list(map(lambda x: x.code, Cie_10Model.query.all()))
        df_cie10 = pd.DataFrame(values, columns=columns)

        # codigo_morfologia
        columns = ['codigo_morfologia']
        values = list(map(lambda x: x.code, CieOMorphologyModel.query.all()))
        df_codigo_morfologia = pd.DataFrame(values, columns=columns)

        # cod_topografia
        columns = ['cod_topografia']
        values = list(map(lambda x: x.code, CieOTopographyModel.query.all()))
        df_cod_topografia = pd.DataFrame(values, columns=columns)

        # cod_localizacion
        columns = ['cod_localizacion']
        values = list(map(lambda x: x.code, CieOTumorLocationModel.query.all()))
        df_cod_localizacion = pd.DataFrame(values, columns=columns)

        # re
        columns = ['re']
        values = ['positive', 'negative', 'no_data']
        df_re = pd.DataFrame(values, columns=columns)

        # rp
        columns = ['rp']
        values = ['positive', 'negative', 'no_data']
        df_rp = pd.DataFrame(values, columns=columns)

        # her2
        columns = ['her2']
        values = list(map(lambda x: x.code, ParameterModel.query.filter_by(domain='HER2_POSITVE').all()))
        df_her2 = pd.DataFrame(values, columns=columns)

        # pais
        columns = ['pais']
        values = list(map(lambda x: x.description, CountryModel.query.all()))
        df_pais = pd.DataFrame(values, columns=columns)

        # departamento
        columns = ['departamento']
        values = list(map(lambda x: x.description, AreaModel.query.all()))
        df_departamento = pd.DataFrame(values, columns=columns)

        # ciudad
        columns = ['ciudad']
        values = list(map(lambda x: x.description, CityModel.query.all()))
        df_ciudad = pd.DataFrame(values, columns=columns)

        # nacionalidad
        columns = ['nacionalidad']
        values = list(map(lambda x: x.nationality, CountryModel.query.all()))
        df_nacionalidad = pd.DataFrame(values, columns=columns)

        # estadocivil
        columns = ['estadocivil']
        values = list(map(lambda x: x.code, ParameterModel.query.filter_by(domain='PATIENT_CIVIL_STATUS')))
        df_estadocivil = pd.DataFrame(values, columns=columns)

        # Crear un objeto BytesIO en memoria para almacenar el archivo Excel
        output = BytesIO()

        # Usar ExcelWriter para escribir en un archivo Excel con múltiples hojas
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Escribir el DataFrame en la primera hoja llamada 'Pacientes'
            df_pacientes.to_excel(writer, sheet_name='Pacientes', index=False)
            # nombre_establecimiento
            df_nombre_establecimiento.to_excel(writer, sheet_name='nombre_establecimiento', index=False)
            # tipo_documento
            df_tipo_documento.to_excel(writer, sheet_name='tipo_documento', index=False)
            # sexo
            df_sexo.to_excel(writer, sheet_name='sexo', index=False)
            # cie10
            df_cie10.to_excel(writer, sheet_name='cie10', index=False)
            # codigo_morfologia
            df_codigo_morfologia.to_excel(writer, sheet_name='codigo_morfologia', index=False)
            # cod_topografia
            df_cod_topografia.to_excel(writer, sheet_name='cod_topografia', index=False)
            # cod_localizacion
            df_cod_localizacion.to_excel(writer, sheet_name='cod_localizacion', index=False)
            # re
            df_re.to_excel(writer, sheet_name='re', index=False)
            # rp
            df_rp.to_excel(writer, sheet_name='rp', index=False)
            # her2
            df_her2.to_excel(writer, sheet_name='her2', index=False)
            # pais
            df_pais.to_excel(writer, sheet_name='pais', index=False)
            # departamento
            df_departamento.to_excel(writer, sheet_name='departamento', index=False)
            # ciudad
            df_ciudad.to_excel(writer, sheet_name='ciudad', index=False)
            # nacionalidad
            df_nacionalidad.to_excel(writer, sheet_name='nacionalidad', index=False)
            # estadocivil
            df_estadocivil.to_excel(writer, sheet_name='estadocivil', index=False)

        # Mover el puntero del archivo al inicio para poder leer su contenido
        output.seek(0)

        # Crear la respuesta HTTP con el archivo Excel
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=pacientes_import.xlsx'
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        return response

    @jwt_required()
    def post(self):
        """
        Método encargado de agregar los Pacientes indicados en el archivo de importación.
        Se admite archivos CSV o Excel.
        :return: Mensaje de éxito o error
        """
        try:
            # Obtener el archivo de importación
            file = request.files.get('file')

            # Validaciones del archivo de importación
            if not file:
                return {'message': _("IMPORT_FILE_NOT_PROVIDED")}, 400

            # Verificar si el archivo es CSV o Excel
            if file.filename.endswith('.csv'):
                df = pd.read_csv(filepath_or_buffer=file)
            elif file.filename.endswith(('.xls', '.xlsx')):
                # Por defecto, toma la primera hoja
                df = pd.read_excel(io=file)
            else:
                return {'message': _("UNSUPPORTED_FILE_FORMAT")}, 400

            # Convertir todos los valores NaN a None en el dataframe
            df = df.applymap(lambda x: None if pd.isna(x) else x)

            # Verificar si las columnas necesarias están presentes
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                return {'message': f'{_("IMPORT_MISSING_COLUMNS")}: {", ".join(missing_columns)}'}, 400

            # Se llevará un regisro de los pacientes no importados
            no_import_patient_list = []

            cipher_key = current_app.config['ENCRYPTION_KEY']

            # Procesar el DataFrame `df` para agregar los pacientes
            for index, row in df.iterrows():
                try:
                    with db.session.no_autoflush:
                        # Obtener los datos de la fila y realizar limpiezas si fuera necesario
                        # Paciente
                        nombre_establecimiento_data = str(row.get('nombre_establecimiento')).strip() if row.get('nombre_establecimiento') else None
                        tipo_documento_data = str(row.get('tipo_documento')).strip() if row.get('tipo_documento') else None
                        documento_nro_data = (str(row.get('documento_nro')).strip() if isinstance(row.get('documento_nro'), int) else row.get('documento_nro')) if row.get('documento_nro') else None
                        nombres_data = str(row.get('nombres')).strip() if row.get('nombres') else None
                        apellidos_data = str(row.get('apellidos')).strip() if row.get('apellidos') else None
                        sexo_data = str(row.get('sexo')).strip() if row.get('sexo') else None
                        fecha_nac_data = parse_date(str(row.get('fecha_nac')).strip() if row.get('fecha_nac') else None)

                        # Diagnostico Anatomía Patológica
                        codigo_morfologia_data = str(row.get('codigo_morfologia')).strip() if row.get('codigo_morfologia') else None
                        clasificacion_data = str(row.get('clasificacion')).strip() if row.get('clasificacion') else None
                        re_data = str(row.get('re')).strip().lower() if str(row.get('re')).strip().lower() in ['positive', 'negative', 'no_data'] else 'no_data'
                        rp_data = str(row.get('rp')).strip().lower() if str(row.get('rp')).strip().lower() in ['positive', 'negative', 'no_data'] else 'no_data'
                        her2_data = str(row.get('her2')).strip().lower() if row.get('her2') else None
                        tamanho_tumor_data = (float(row.get('tamanho_tumor').strip()) if isinstance(row['tamanho_tumor'], str) else row.get('tamanho_tumor')) if row.get('tamanho_tumor') else None
                        cod_topografia_data = str(row.get('cod_topografia')).strip() if row.get('cod_topografia') else None
                        cod_localizacion_data = str(row.get('cod_localizacion')).strip() if row.get('cod_localizacion') else None
                        material_data = str(row.get('material')).strip() if row.get('material') else None
                        dx_presuntivo_data = str(row.get('dx_presuntivo')).strip() if row.get('dx_presuntivo') else None
                        macroscopia_data = str(row.get('macroscopia')).strip() if row.get('macroscopia') else None
                        microscopia_data = str(row.get('microscopia')).strip() if row.get('microscopia') else None
                        diagnostico_data = str(row.get('diagnostico')).strip() if row.get('diagnostico') else None
                        fecha_dx_ap_data = parse_date(str(row.get('fecha_dx_ap')).strip() if row.get('fecha_dx_ap') else None)

                        # Diagnostico
                        cie10_data = str(row.get('cie10')).strip() if row.get('cie10') else None
                        fecha_dx_data = parse_date(str(row.get('fecha_dx')).strip() if row.get('fecha_dx') else None)

                        # Datos no macheados
                        complementario_data = str(row.get('complementario')).strip() if row.get('complementario') else None
                        idsolicitud_data = int(row.get('idsolicitud')) if row.get('idsolicitud') else None
                        fecha_validacion_data = parse_date(str(row.get('fecha_validacion')).strip() if row.get('fecha_validacion') else None)

                        # Datos Complementarios de Paciente
                        direccion_data = str(row.get('direccion')).strip() if row.get('direccion') else None
                        pais_data = str(row.get('pais')).strip() if row.get('pais') else None
                        departamento_data = str(row.get('departamento')).strip() if row.get('departamento') else None
                        ciudad_data = str(row.get('ciudad')).strip() if row.get('ciudad') else None
                        telefono_data = str(row.get('telefono')).strip() if row.get('telefono') else None
                        nacionalidad_data = str(row.get('nacionalidad')).strip() if row.get('nacionalidad') else None
                        estadocivil_data = str(row.get('estadocivil')).strip() if row.get('estadocivil') else None
                        nro_ficha_data = str(row.get('nro_ficha')).strip() if row.get('nro_ficha') else None

                        # Verificar si ya existe un paciente con el mismo documento_nro y tipo_documento
                        tipo_documento: DocumentTypeModel = DocumentTypeModel.query.filter_by(code=tipo_documento_data).first()
                        if tipo_documento:
                            patient_model: PatientModel = PatientModel.query.filter(
                                PatientModel.document_type_id == tipo_documento.id,
                                func.decrypt_data(PatientModel.document_number, cipher_key) == documento_nro_data).first()
                        else:
                            tipo_documento = DocumentTypeModel.query.filter_by(code='CI').first()   # Por defecto CI
                            patient_model: PatientModel = PatientModel.query.filter(
                                func.decrypt_data(PatientModel.document_number, cipher_key) == documento_nro_data).first()

                        hospital_model = None
                        if nombre_establecimiento_data:
                            hospital_model = HospitalModel.query.filter_by(description=nombre_establecimiento_data).first()

                        if not patient_model:
                            # Crear un nuevo paciente
                            patient_model: PatientModel = PatientModel()

                            # Datos requeridos por archivo de importación
                            patient_model.document_type = tipo_documento
                            patient_model.document_number = documento_nro_data
                            patient_model.firstname = nombres_data
                            patient_model.lastname = apellidos_data
                            patient_model.birthdate = fecha_nac_data
                            patient_model.gender = GenderModel.query.filter_by(code=sexo_data).first() if sexo_data else None
                            if hospital_model:
                                patient_hospital_ids = list(map(lambda x: x.id, patient_model.hospital_list))
                                if not hospital_model.id in patient_hospital_ids:
                                    pat_hos = PatientHospitalModel()
                                    pat_hos.hospital_id = hospital_model.id
                                    patient_model.hospital_list.append(pat_hos)

                            # Otros datos
                            patient_status = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='SOSP').first()
                            if patient_status:
                                patient_model.state = patient_status
                            patient_vital_status = ParameterModel.query.filter_by(domain='PATIENT_VITAL_STATE', code='V').first()
                            if patient_status:
                                patient_model.vital_state = patient_vital_status
                            patient_model.registration_date = datetime.now()
                            patient_model.origin = OriginsCode.CCAN_CITY_SOFT.value
                            patient_model.user_create = 'import'

                            # Datos Complementarios
                            patient_model.address = direccion_data
                            patient_model.country = CountryModel.query.filter_by(description=pais_data).first() if pais_data else None
                            patient_model.area = AreaModel.query.filter_by(description=departamento_data).first() if departamento_data else None
                            patient_model.city = CityModel.query.filter_by(description=ciudad_data).first() if ciudad_data else None
                            patient_model.phone = telefono_data
                            patient_model.nationality = CountryModel.query.filter_by(nationality=nacionalidad_data).first() if nacionalidad_data else None
                            patient_model.civil_status = ParameterModel.query.filter_by(domain='PATIENT_CIVIL_STATUS', code=estadocivil_data).first() if estadocivil_data else None
                            patient_model.number_card = nro_ficha_data

                            # Paso necesario antes de grabar un paciente
                            patient_model.encript_data()
                            db.session.add(patient_model)

                            # Generar id den BD
                            db.session.flush()

                        # Datos de filtro
                        patient_id = patient_model.id

                        # Datos de Diagnóstico
                        fecha_dx = fecha_dx_data
                        if fecha_dx:
                            # Validación de duplicidad
                            diagnosis_object = DiagnosisModel.query.filter_by(patient_id=patient_id, date=fecha_dx).first()
                            # Si el registro ya no fue insertado anteriormente
                            diagnosis_model: DiagnosisModel = diagnosis_object if diagnosis_object else DiagnosisModel()

                            diagnosis_model.date = fecha_dx
                            diagnosis_model.patient_id = patient_model.id
                            diagnosis_model.cie_10 = Cie_10Model.query.filter_by(code=cie10_data).first() if cie10_data else None
                            diagnosis_model.cie_o_morphology = CieOMorphologyModel.query.filter_by(code=codigo_morfologia_data).first() if codigo_morfologia_data else None
                            diagnosis_model.cie_o_topography = CieOTopographyModel.query.filter_by(code=cod_topografia_data).first() if cod_topografia_data else None
                            diagnosis_model.cie_o_tumor_location = CieOTumorLocationModel.query.filter_by(code=cod_localizacion_data).first() if cod_localizacion_data else None
                            diagnosis_model.user_create = 'import'
                            diagnosis_model.hospital = hospital_model
                            db.session.add(diagnosis_model)

                        # Datos de Diagnóstico Anatomía Patológica
                        # Validación de duplicidad
                        fecha_dx_ap = fecha_dx_ap_data
                        if fecha_dx_ap:
                            diagnosis_ap_object = DiagnosisApModel.query.filter_by(patient_id=patient_id, date=fecha_dx_ap).first()
                            # Si el registro ya no fue insertado anteriormente
                            diagnosis_ap_model: DiagnosisApModel = diagnosis_ap_object if diagnosis_ap_object else DiagnosisApModel()

                            diagnosis_ap_model.patient_id = patient_id
                            diagnosis_ap_model.date = fecha_dx_ap
                            diagnosis_ap_model.hospital = hospital_model
                            diagnosis_ap_model.cie_o_morphology = CieOMorphologyModel.query.filter_by(code=codigo_morfologia_data).first() if codigo_morfologia_data else None
                            diagnosis_ap_model.cie_o_topography = CieOTopographyModel.query.filter_by(code=cod_topografia_data).first() if cod_topografia_data else None
                            diagnosis_ap_model.cie_o_tumor_location = CieOTumorLocationModel.query.filter_by( code=cod_localizacion_data).first() if cod_localizacion_data else None
                            diagnosis_ap_model.armpit = 'no_data'
                            diagnosis_ap_model.re = re_data
                            diagnosis_ap_model.rp = rp_data
                            diagnosis_ap_model.her2 = 'positive' if her2_data else 'no_data'
                            diagnosis_ap_model.her2_positive = ParameterModel.query.filter_by(domain='HER2_POSITVE', code=her2_data).first() if her2_data else None
                            diagnosis_ap_model.tumor_size = tamanho_tumor_data
                            diagnosis_ap_model.user_create = 'import'
                            diagnosis_ap_model.origin = OriginsCode.CCAN_CITY_SOFT.value

                            # Campos de Reporte General
                            diagnosis_ap_model.dx_presuntivo = dx_presuntivo_data
                            diagnosis_ap_model.material = material_data
                            diagnosis_ap_model.diagnostico = diagnostico_data
                            diagnosis_ap_model.clasificacion = clasificacion_data
                            diagnosis_ap_model.macroscopia = macroscopia_data
                            diagnosis_ap_model.microscopia = microscopia_data
                            db.session.add(diagnosis_ap_model)

                        # Se persisten todos los cambios
                        db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    logging.error(f"{_('IMPORT_NOT_INSERTING_PATIENT')} {documento_nro_data} due to: {error}")
                    no_import_patient_list.append(documento_nro_data)

            return_status = 200 if len(no_import_patient_list) == 0 else 400
            msg_no_imported = f" {_('IMPORT_NO_IMPORTED')}: {len(no_import_patient_list)} {_('IMPORT_ROWS')}." if len(no_import_patient_list) > 0 else ''
            return {'message': f"{_('IMPORT_FILE_PROCESSED')}.{msg_no_imported}"}, return_status

        except Exception as e:
            return {'message': f'Error during import: {str(e)}'}, 500
