import json
import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_babel import _
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import desc, asc

from db import db
from models.cervix_form import CervixFormModel
from models.diagnosis import DiagnosisModel
from models.medical_document import MedicalDocumentModel
from models.patient import PatientModel
from models.patient_family_with_cancer import PatientFamilyWithCancerModel
from models.personal_pathological_history import PersonalPathologicalHistoryModel
from resources.medical_document import persist_document
from security import check
from utils import restrict, paginated_results, validate_json_parser

FILE_MODULE = 'cervix_forms'


class CervixForm(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('departament', type=str)
    parser.add_argument('parity', type=bool)
    parser.add_argument('residential_address', type=str)
    parser.add_argument('pmhx', type=str)
    parser.add_argument('presenting_complaint', type=str)
    parser.add_argument('main_physical_clinical_findings', type=str)
    parser.add_argument('performance_status_ecog_id', type=int)
    parser.add_argument('treatment_decision', type=str)
    parser.add_argument('colposcopy_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('colposcopy_report_id', type=int)
    parser.add_argument('cervical_biopsy_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('cervical_biopsy_histology', type=str)
    parser.add_argument('cervical_biopsy_morphology', type=str)
    parser.add_argument('cervical_biopsy_grade', type=str)
    parser.add_argument('usg_pelvis_abdomen_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('usg_pelvis_abdomen_site_of_mass_id', type=int)
    parser.add_argument('usg_pelvis_abdomen_size_of_mass', type=str)
    parser.add_argument('usg_pelvis_abdomen_extensions_id', type=int)
    parser.add_argument('chest_xray_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('chest_xray_report_id', type=int)
    parser.add_argument('chest_xray_summary_id', type=int)
    parser.add_argument('pelvic_mri_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('pelvic_mri_site_of_mass_id', type=int)
    parser.add_argument('pelvic_mri_size_of_mass', type=str)
    parser.add_argument('pelvic_mri_extensions_id', type=int)
    parser.add_argument('blood_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('blood_fbc_id', type=int)
    parser.add_argument('blood_fbc', type=str)
    parser.add_argument('blood_lft_report_id', type=int)
    parser.add_argument('blood_urea_creatinine_report_id', type=int)
    parser.add_argument('stage_figo_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('stage_figo_id', type=int)
    parser.add_argument('stage_figo_i_id', type=int)
    parser.add_argument('stage_figo_ia_id', type=int)
    parser.add_argument('stage_figo_ib_id', type=int)
    parser.add_argument('stage_figo_ii_id', type=int)
    parser.add_argument('stage_figo_iii_id', type=int)
    parser.add_argument('stage_figo_iv_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_modify', type=str)


    @jwt_required()
    @check('cervix_form_get')
    @swag_from('../swagger/cervix_form/get_cervix_form.yaml')
    def get(self, id):
        cervix_form = CervixFormModel.find_by_id(id)
        if cervix_form:
            return cervix_form.json()
        return {'message': _("CERVIX_FORM_NOT_FOUND")}, 404

    @jwt_required()
    @check('cervix_form_update')
    @swag_from('../swagger/cervix_form/put_cervix_form.yaml')
    def put(self, id):
        cervix_form = CervixFormModel.find_by_id(id)
        if not cervix_form:
            return {'message': _("CERVIX_FORM_NOT_FOUND")}, 404

        # Obtener datos JSON
        json_data = request.form.get('json')
        if json_data:
            json_data = json.loads(json_data)

        # Obtener archivos
        files = request.files

        try:
            with db.session.no_autoflush:
                newdata = validate_json_parser(CervixForm.parser, json_data)

                # Process documents
                # Delete
                keys = list(newdata.keys())
                documents_file_keys = [field for field in keys if field.endswith('_report')]
                for key in documents_file_keys:
                    if newdata[key].get('delete'):
                        setattr(cervix_form, f"{key}_id", None)

                # New
                for fileKey in files:
                    file = files[fileKey]
                    path = persist_document(file, FILE_MODULE)
                    if path:
                        medical_document_model = MedicalDocumentModel()
                        medical_document_model.description = None
                        medical_document_model.path = path
                        medical_document_model.patient_id = newdata.get('patient_id')
                        medical_document_model.medical_document_type_id = json_data.get(fileKey, {}).get('medical_document_type_id')
                        medical_document_model.modulo = FILE_MODULE
                        medical_document_model.origen_id = None
                        medical_document_model.study_date = None
                        medical_document_model.user_create = get_jwt_identity()
                        medical_document_model.date_modify = None
                        medical_document_model.user_modify = None
                        medical_document_model.hospital_id = None
                        db.session.add(medical_document_model)
                        db.session.flush()
                        newdata[f"{fileKey}_id"] = medical_document_model.id

                CervixFormModel.from_reqparse(cervix_form, newdata, with_none=True)
                cervix_form.user_modify = get_jwt_identity()
                cervix_form.date_modify = datetime.now()
                db.session.add(cervix_form)

                # Persist Header
                saveCervixBreastHeaderForm(newdata.get('patient_id'), json_data.get('header'))

                # Se persisten los cambios
                db.session.commit()
        except Exception as e:
            # Se revierten los cambios
            db.session.rollback()

            logging.error(_("CERVIX_FORM_UPDATE_ERROR"), exc_info=e)
            return {"message": _("CERVIX_FORM_UPDATE_ERROR")}, 500

        return cervix_form.json()


    @jwt_required()
    @check('cervix_form_delete')
    @swag_from('../swagger/cervix_form/delete_cervix_form.yaml')
    def delete(self, id):
        cervix_form = CervixFormModel.find_by_id(id)
        if cervix_form:
            cervix_form.delete_from_db()

        return {'message': _("CERVIX_FORM_DELETED")}


class CervixFormList(Resource):

    @jwt_required()
    @check('cervix_form_list')
    @swag_from('../swagger/cervix_form/list_cervix_form.yaml')
    def get(self):
        query = CervixFormModel.query
        return paginated_results(query)

    @jwt_required()
    @check('cervix_form_insert')
    @swag_from('../swagger/cervix_form/post_cervix_form.yaml')
    def post(self):
        # Obtener datos JSON
        json_data = request.form.get('json')
        if json_data:
            json_data = json.loads(json_data)

        # Obtener archivos
        files = request.files

        data = validate_json_parser(CervixForm.parser, json_data)

        # Validaciones
        id = data.get('id')
        if id is not None and CervixFormModel.find_by_id(id):
            return {'message': _("CERVIX_FORM_DUPLICATED").format(id)}, 400

        patient_id = data.get('patient_id')
        cervix_form_model = CervixFormModel.query.filter_by(patient_id=patient_id).first()
        if cervix_form_model:
            return {'message': _("CERVIX_FORM_DUPLICATED").format(id)}, 400

        try:
            with db.session.no_autoflush:
                # Process documents
                for fileKey in files:
                    file = files[fileKey]
                    path = persist_document(file, FILE_MODULE)
                    if path:
                        medical_document_model = MedicalDocumentModel()
                        medical_document_model.description = None
                        medical_document_model.path = path
                        medical_document_model.patient_id = data.get('patient_id')
                        medical_document_model.medical_document_type_id = json_data.get(fileKey, {}).get('medical_document_type_id')
                        medical_document_model.modulo = FILE_MODULE
                        medical_document_model.origen_id = None
                        medical_document_model.study_date = None
                        medical_document_model.user_create = get_jwt_identity()
                        medical_document_model.date_modify = None
                        medical_document_model.user_modify = None
                        medical_document_model.hospital_id = None
                        db.session.add(medical_document_model)
                        db.session.flush()
                        data[f"{fileKey}_id"] = medical_document_model.id

                # Se elimina claves de reporte
                keys = list(data.keys())
                documents_file_keys = [field for field in keys if field.endswith('_report')]
                for key in documents_file_keys:
                    del data[key]

                cervix_form: CervixFormModel = CervixFormModel(**data)
                cervix_form.user_create = get_jwt_identity()
                db.session.add(cervix_form)

                # Persist Header
                patient_id = data.get('patient_id')
                header = json_data.get('header')
                saveCervixBreastHeaderForm(patient_id, header)

                # Se persisten los cambios
                db.session.commit()
        except Exception as e:
            # Se revierten los cambios
            db.session.rollback()

            logging.error(_("CERVIX_FORM_CREATE_ERROR"), exc_info=e)
            return {"message": _("CERVIX_FORM_CREATE_ERROR")}, 500

        return cervix_form.json(), 201


class CervixFormSearch(Resource):

    @jwt_required()
    @check('cervix_form_search')
    @swag_from('../swagger/cervix_form/search_cervix_form.yaml')
    def post(self):
        query = CervixFormModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: CervixFormModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: CervixFormModel.patient_id == x)
            query = restrict(query, filters, 'departament', lambda x: CervixFormModel.departament.contains(x))
            query = restrict(query, filters, 'parity', lambda x: x)
            query = restrict(query, filters, 'residential_address', lambda x: CervixFormModel.residential_address.contains(x))
            query = restrict(query, filters, 'pmhx', lambda x: CervixFormModel.pmhx.contains(x))
            query = restrict(query, filters, 'presenting_complaint', lambda x: CervixFormModel.presenting_complaint.contains(x))
            query = restrict(query, filters, 'main_physical_clinical_findings', lambda x: CervixFormModel.main_physical_clinical_findings.contains(x))
            query = restrict(query, filters, 'performance_status_ecog_id', lambda x: CervixFormModel.performance_status_ecog_id == x)
            query = restrict(query, filters, 'treatment_decision', lambda x: CervixFormModel.treatment_decision.contains(x))
            query = restrict(query, filters, 'colposcopy_report_id', lambda x: CervixFormModel.colposcopy_report_id == x)
            query = restrict(query, filters, 'cervical_biopsy_histology', lambda x: CervixFormModel.cervical_biopsy_histology.contains(x))
            query = restrict(query, filters, 'cervical_biopsy_morphology', lambda x: CervixFormModel.cervical_biopsy_morphology.contains(x))
            query = restrict(query, filters, 'cervical_biopsy_grade', lambda x: CervixFormModel.cervical_biopsy_grade.contains(x))
            query = restrict(query, filters, 'usg_pelvis_abdomen_site_of_mass_id', lambda x: CervixFormModel.usg_pelvis_abdomen_site_of_mass_id == x)
            query = restrict(query, filters, 'usg_pelvis_abdomen_size_of_mass', lambda x: CervixFormModel.usg_pelvis_abdomen_size_of_mass.contains(x))
            query = restrict(query, filters, 'usg_pelvis_abdomen_extensions_id', lambda x: CervixFormModel.usg_pelvis_abdomen_extensions_id == x)
            query = restrict(query, filters, 'chest_xray_report_id', lambda x: CervixFormModel.chest_xray_report_id == x)
            query = restrict(query, filters, 'chest_xray_summary_id', lambda x: CervixFormModel.chest_xray_summary_id == x)
            query = restrict(query, filters, 'pelvic_mri_site_of_mass_id', lambda x: CervixFormModel.pelvic_mri_site_of_mass_id == x)
            query = restrict(query, filters, 'pelvic_mri_size_of_mass', lambda x: CervixFormModel.pelvic_mri_size_of_mass.contains(x))
            query = restrict(query, filters, 'pelvic_mri_extensions_id', lambda x: CervixFormModel.pelvic_mri_extensions_id == x)
            query = restrict(query, filters, 'blood_fbc_id', lambda x: CervixFormModel.blood_fbc_id == x)
            query = restrict(query, filters, 'blood_fbc', lambda x: CervixFormModel.blood_fbc.contains(x))
            query = restrict(query, filters, 'blood_lft_report_id', lambda x: CervixFormModel.blood_lft_report_id == x)
            query = restrict(query, filters, 'blood_urea_creatinine_report_id', lambda x: CervixFormModel.blood_urea_creatinine_report_id == x)
            query = restrict(query, filters, 'stage_figo_id', lambda x: CervixFormModel.stage_figo_id == x)
            query = restrict(query, filters, 'stage_figo_i_id', lambda x: CervixFormModel.stage_figo_i_id == x)
            query = restrict(query, filters, 'stage_figo_ia_id', lambda x: CervixFormModel.stage_figo_ia_id == x)
            query = restrict(query, filters, 'stage_figo_ib_id', lambda x: CervixFormModel.stage_figo_ib_id == x)
            query = restrict(query, filters, 'stage_figo_ii_id', lambda x: CervixFormModel.stage_figo_ii_id == x)
            query = restrict(query, filters, 'stage_figo_iii_id', lambda x: CervixFormModel.stage_figo_iii_id == x)
            query = restrict(query, filters, 'stage_figo_iv_id', lambda x: CervixFormModel.stage_figo_iv_id == x)
            query = restrict(query, filters, 'user_create', lambda x: CervixFormModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: CervixFormModel.user_modify.contains(x))

        # default order
        query = query.order_by(CervixFormModel.id.desc())
        return paginated_results(query)


class CervixBreastHeaderForm(Resource):
    @jwt_required()
    # @check('cervix_breast_header_form_get')
    # @swag_from('../swagger/cervix_form/cervix_breast_header_form_get.yaml')
    def get(self, patient_id):
        patient_model = PatientModel.find_by_id(patient_id)
        if not patient_model:
            return {'message': 'No se encuentra Cervix_form'}, 404

        # Prepare response
        # Patient
        patient_json = patient_model.json(1)

        # Personal Pathological History (last row)
        personal_pathological_history_model = (PersonalPathologicalHistoryModel.query
                                               .filter(PersonalPathologicalHistoryModel.patient_id == patient_id)
                                               .order_by(desc(PersonalPathologicalHistoryModel.date_create))
                                               .first())
        personal_pathological_history_json = {}
        if personal_pathological_history_model:
            personal_pathological_history_json = personal_pathological_history_model.json(1)

        # Diagnosis (first row)
        diagnosis_model = (DiagnosisModel.query
                           .filter(DiagnosisModel.patient_id == patient_id)
                           .order_by(asc(DiagnosisModel.date))
                           .first())
        diagnosis_json = {}
        if diagnosis_model:
            diagnosis_json = diagnosis_model.json()

        response = {
            'hospital_list': patient_json.get('hospital_list'),
            'document_type_id': patient_json.get('document_type_id'),
            'document_number': patient_json.get('document_number'),
            'birthdate': patient_json.get('birthdate'),
            'gender_id': patient_json.get('gender_id'),
            'first_diagnosis_date': diagnosis_json.get('date'),
            'folder_number': patient_json.get('number_card'),
            'menopausal_status_id': personal_pathological_history_json.get('menopausal_state_id'),
            'family_members_with_cancer': personal_pathological_history_json.get('family_members_with_cancer'),
            'family_list': personal_pathological_history_json.get('family_list'),
            'civil_status_id': patient_json.get('civil_status_id'),
            'address': patient_json.get('address'),
            'country_id': patient_json.get('country_id'),
            'area_id': patient_json.get('area_id'),
            'city_id': patient_json.get('city_id'),
            'phone': patient_json.get('phone'),
            'next_of_kin_firstname': patient_json.get('responsible_firstname'),
            'next_of_kin_lastname': patient_json.get('responsible_lastname'),
            'next_of_kin_relationship': patient_json.get('responsible_relationship'),
            'next_of_kin_phone': patient_json.get('responsible_phone'),
        }

        return response, 200


def saveCervixBreastHeaderForm(patient_id, data):
    patient_model: PatientModel = PatientModel.find_by_id(patient_id)
    if patient_model:
        patient_json = patient_model.json()
        patient_model.firstname = patient_json.get('firstname')
        patient_model.lastname = patient_json.get('lastname')
        patient_model.document_type_id = data.get('document_type_id')
        patient_model.document_number = data.get('document_number')
        patient_model.birthdate = datetime.strptime(data.get('birthdate'), '%d/%m/%Y') if data.get('birthdate') else None
        patient_model.gender_id = data.get('gender_id')
        patient_model.number_card = data.get('folder_number')
        patient_model.civil_status_id = data.get('civil_status_id')
        patient_model.address = data.get('address')
        patient_model.country_id = data.get('country_id')
        patient_model.area_id = data.get('area_id')
        patient_model.city_id = data.get('city_id')
        patient_model.phone = data.get('phone')
        patient_model.responsible_firstname = data.get('next_of_kin_firstname')
        patient_model.responsible_lastname = data.get('next_of_kin_lastname')
        patient_model.responsible_relationship = data.get('next_of_kin_relationship')
        patient_model.next_of_kin_phone = data.get('responsible_phone')
        patient_model.encript_data()
        db.session.add(patient_model)

    # Personal Pathological History (last row)
    personal_pathological_history_model = (PersonalPathologicalHistoryModel.query
                                           .filter(PersonalPathologicalHistoryModel.patient_id == patient_id)
                                           .order_by(desc(PersonalPathologicalHistoryModel.date_create))
                                           .first())
    if personal_pathological_history_model:
        personal_pathological_history_model.menopausal_state_id = data.get('menopausal_status_id')
        personal_pathological_history_model.family_members_with_cancer = data.get('family_members_with_cancer')
        if personal_pathological_history_model.family_members_with_cancer == 'yes':
            family_list = []
            family_data_list = data.get('family_list')
            for family_data in family_data_list:
                if family_data.get('id'):
                    family_model = PatientFamilyWithCancerModel.find_by_id(family_data.get('id'))
                    PatientFamilyWithCancerModel.from_reqparse(family_model, family_data)
                else:
                    family_model = PatientFamilyWithCancerModel(**family_data)
                family_list.append(family_model)
            personal_pathological_history_model.family_list = family_list
        else:
            personal_pathological_history_model.family_list = []
        db.session.add(personal_pathological_history_model)

    # Diagnosis (first row)
    diagnosis_model = (DiagnosisModel.query
                       .filter(DiagnosisModel.patient_id == patient_id)
                       .order_by(asc(DiagnosisModel.date))
                       .first())
    if diagnosis_model:
        diagnosis_model.date = datetime.strptime(data.get('first_diagnosis_date'), '%d/%m/%Y') if data.get('first_diagnosis_date') else None
        db.session.add(diagnosis_model)

    # Se persisten los cambios
    db.session.commit()
