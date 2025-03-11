import base64
import json
import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_babel import _
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from db import db
from models.breast_form import BreastFormModel
from models.medical_document import MedicalDocumentModel
from resources.cervix_form import saveCervixBreastHeaderForm
from resources.medical_document import persist_document
from utils import restrict, paginated_results, validate_json_parser
from security import check

FILE_MODULE = 'breast_form'


class BreastForm(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('departament', type=str)
    parser.add_argument('residential_address', type=str)
    parser.add_argument('parity', type=bool)
    parser.add_argument('pmhx', type=str)
    parser.add_argument('presenting_complaint', type=str)
    parser.add_argument('main_physical_clinical_findings', type=str)
    parser.add_argument('performance_status_ecog_id', type=int)
    parser.add_argument('treatment_decision', type=str)
    parser.add_argument('mammogram_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('mammogram_birads_id', type=int)
    parser.add_argument('mammogram_report_id', type=int)
    parser.add_argument('usg_breast_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('usg_breast_birads_id', type=int)
    parser.add_argument('usg_breast_report_id', type=int)
    parser.add_argument('fnac_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('fnac_report_id', type=int)
    parser.add_argument('fnac_summary', type=str)
    parser.add_argument('trucut_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('trucut_histology_report_id', type=int)
    parser.add_argument('trucut_morphology_id', type=int)
    parser.add_argument('trucut_others', type=str)
    parser.add_argument('trucut_grade', type=str)
    parser.add_argument('trucut_hormone_receptor_status_id', type=int)
    parser.add_argument('trucut_her2_neu_id', type=int)
    parser.add_argument('other_biopsy_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('other_biopsy_histology_report_id', type=int)
    parser.add_argument('other_biopsy_morphology_id', type=int)
    parser.add_argument('other_biopsy_others', type=str)
    parser.add_argument('other_biopsy_grade', type=str)
    parser.add_argument('other_biopsy_hormone_receptor_status_id', type=int)
    parser.add_argument('other_biopsy_her2_neu_id', type=int)
    parser.add_argument('chest_xray_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('chest_xray_report_id', type=int)
    parser.add_argument('chest_xray_summary_id', type=int)
    parser.add_argument('chest_ct_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('chest_ct_report_id', type=int)
    parser.add_argument('chest_ct_summary_id', type=int)
    parser.add_argument('usg_liver_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('usg_liver_summary_id', type=int)
    parser.add_argument('blood_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('blood_fbc_id', type=int)
    parser.add_argument('blood_fbc', type=str)
    parser.add_argument('blood_fbc_report_id', type=int)
    parser.add_argument('blood_lft_report_id', type=int)
    parser.add_argument('blood_urea_creatinine_report_id', type=int)
    parser.add_argument('bone_scan_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('bone_scan_summary', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_modify', type=str)
    parser.add_argument('stage_breast_location_id', type=int)
    parser.add_argument('stage_breast_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('stage_breast_t_id', type=int)
    parser.add_argument('stage_breast_n_id', type=int)
    parser.add_argument('stage_breast_m_id', type=int)

    @jwt_required()
    @check('breast_form_get')
    @swag_from('../swagger/breast_form/get_breast_form.yaml')
    def get(self, id):
        breast_form = BreastFormModel.find_by_id(id)
        if breast_form:
            return breast_form.json()
        return {'message': _("BREAST_FORM_NOT_FOUND")}, 404

    @jwt_required()
    @check('breast_form_update')
    @swag_from('../swagger/breast_form/put_breast_form.yaml')
    def put(self, id):
        breast_form = BreastFormModel.find_by_id(id)
        if not breast_form:
            return {'message': _("BREAST_FORM_NOT_FOUND")}, 404

        # Obtener datos JSON
        json_data = request.form.get('json')
        if json_data:
            json_data = json.loads(json_data)

        # Obtener archivos
        files = request.files

        try:
            with db.session.no_autoflush:
                newdata = validate_json_parser(BreastForm.parser, json_data)

                # Process documents
                # Delete
                keys = list(newdata.keys())
                documents_file_keys = [field for field in keys if field.endswith('_report')]
                for key in documents_file_keys:
                    if newdata[key].get('delete'):
                        setattr(breast_form, f"{key}_id", None)

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
                        print(fileKey)
                        db.session.flush()
                        newdata[f"{fileKey}_id"] = medical_document_model.id

                BreastFormModel.from_reqparse(breast_form, newdata, with_none=True)
                breast_form.user_modify = get_jwt_identity()
                breast_form.date_modify = datetime.now()
                db.session.add(breast_form)

                # Persist Header
                saveCervixBreastHeaderForm(newdata.get('patient_id'), json_data.get('header'))

                # Se persisten los cambios
                db.session.commit()
        except Exception as e:
            # Se revierten los cambios
            db.session.rollback()

            logging.error(_("BREAST_FORM_UPDATE_ERROR"), exc_info=e)
            return {"message": _("BREAST_FORM_UPDATE_ERROR")}, 500

        return breast_form.json()



    @jwt_required()
    @check('breast_form_delete')
    @swag_from('../swagger/breast_form/delete_breast_form.yaml')
    def delete(self, id):
        breast_form = BreastFormModel.find_by_id(id)
        if breast_form:
            breast_form.delete_from_db()

        return {'message': _("BREAST_FORM_DELETED")}


class BreastFormList(Resource):

    @jwt_required()
    @check('breast_form_list')
    @swag_from('../swagger/breast_form/list_breast_form.yaml')
    def get(self):
        query = BreastFormModel.query
        return paginated_results(query)

    @jwt_required()
    @check('breast_form_insert')
    @swag_from('../swagger/breast_form/post_breast_form.yaml')
    def post(self):
        # Obtener datos JSON
        json_data = request.form.get('json')
        if json_data:
            json_data = json.loads(json_data)

        # Obtener archivos
        files = request.files

        data = validate_json_parser(BreastForm.parser, json_data)

        # Validaciones
        id = data.get('id')
        if id is not None and BreastFormModel.find_by_id(id):
            return {'message': _("BREAST_FORM_DUPLICATED").format(id)}, 400

        patient_id = data.get('patient_id')
        breast_form_model = BreastFormModel.query.filter_by(patient_id=patient_id).first()
        if breast_form_model:
            return {'message': _("BREAST_FORM_DUPLICATED").format(id)}, 400

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

                breast_form: BreastFormModel = BreastFormModel(**data)
                breast_form.user_create = get_jwt_identity()
                db.session.add(breast_form)

                # Persist Header
                patient_id = data.get('patient_id')
                header = json_data.get('header')
                saveCervixBreastHeaderForm(patient_id, header)

                # Se persisten los cambios
                db.session.commit()
        except Exception as e:
            # Se revierten los cambios
            db.session.rollback()

            logging.error(_("BREAST_FORM_CREATE_ERROR"), exc_info=e)
            return {"message": _("BREAST_FORM_CREATE_ERROR")}, 500

        return breast_form.json(), 201


class BreastFormSearch(Resource):

    @jwt_required()
    @check('breast_form_search')
    @swag_from('../swagger/breast_form/search_breast_form.yaml')
    def post(self):
        query = BreastFormModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: BreastFormModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: BreastFormModel.patient_id == x)
            query = restrict(query, filters, 'departament', lambda x: BreastFormModel.departament.contains(x))
            query = restrict(query, filters, 'residential_address', lambda x: BreastFormModel.residential_address.contains(x))
            query = restrict(query, filters, 'parity', lambda x: x)
            query = restrict(query, filters, 'pmhx', lambda x: BreastFormModel.pmhx.contains(x))
            query = restrict(query, filters, 'presenting_complaint', lambda x: BreastFormModel.presenting_complaint.contains(x))
            query = restrict(query, filters, 'main_physical_clinical_findings', lambda x: BreastFormModel.main_physical_clinical_findings.contains(x))
            query = restrict(query, filters, 'performance_status_ecog_id', lambda x: BreastFormModel.performance_status_ecog_id == x)
            query = restrict(query, filters, 'treatment_decision', lambda x: BreastFormModel.treatment_decision.contains(x))
            query = restrict(query, filters, 'mammogram_birads_id', lambda x: BreastFormModel.mammogram_birads_id == x)
            query = restrict(query, filters, 'mammogram_report_id', lambda x: BreastFormModel.mammogram_report_id == x)
            query = restrict(query, filters, 'usg_breast_birads_id', lambda x: BreastFormModel.usg_breast_birads_id == x)
            query = restrict(query, filters, 'usg_breast_report_id', lambda x: BreastFormModel.usg_breast_report_id == x)
            query = restrict(query, filters, 'fnac_report_id', lambda x: BreastFormModel.fnac_report_id == x)
            query = restrict(query, filters, 'fnac_summary', lambda x: BreastFormModel.fnac_summary.contains(x))
            query = restrict(query, filters, 'trucut_histology_report_id', lambda x: BreastFormModel.trucut_histology_report_id == x)
            query = restrict(query, filters, 'trucut_morphology_id', lambda x: BreastFormModel.trucut_morphology_id == x)
            query = restrict(query, filters, 'trucut_others', lambda x: BreastFormModel.trucut_others.contains(x))
            query = restrict(query, filters, 'trucut_grade', lambda x: BreastFormModel.trucut_grade.contains(x))
            query = restrict(query, filters, 'trucut_hormone_receptor_status_id', lambda x: BreastFormModel.trucut_hormone_receptor_status_id == x)
            query = restrict(query, filters, 'trucut_her2_neu_id', lambda x: BreastFormModel.trucut_her2_neu_id == x)
            query = restrict(query, filters, 'other_biopsy_histology_report_id', lambda x: BreastFormModel.other_biopsy_histology_report_id == x)
            query = restrict(query, filters, 'other_biopsy_morphology_id', lambda x: BreastFormModel.other_biopsy_morphology_id == x)
            query = restrict(query, filters, 'other_biopsy_others', lambda x: BreastFormModel.other_biopsy_others.contains(x))
            query = restrict(query, filters, 'other_biopsy_grade', lambda x: BreastFormModel.other_biopsy_grade.contains(x))
            query = restrict(query, filters, 'other_biopsy_hormone_receptor_status_id', lambda x: BreastFormModel.other_biopsy_hormone_receptor_status_id == x)
            query = restrict(query, filters, 'other_biopsy_her2_neu_id', lambda x: BreastFormModel.other_biopsy_her2_neu_id == x)
            query = restrict(query, filters, 'chest_xray_report_id', lambda x: BreastFormModel.chest_xray_report_id == x)
            query = restrict(query, filters, 'chest_xray_summary_id', lambda x: BreastFormModel.chest_xray_summary_id == x)
            query = restrict(query, filters, 'chest_ct_report_id', lambda x: BreastFormModel.chest_ct_report_id == x)
            query = restrict(query, filters, 'chest_ct_summary_id', lambda x: BreastFormModel.chest_ct_summary_id == x)
            query = restrict(query, filters, 'usg_liver_summary_id', lambda x: BreastFormModel.usg_liver_summary_id == x)
            query = restrict(query, filters, 'blood_fbc_id', lambda x: BreastFormModel.blood_fbc_id == x)
            query = restrict(query, filters, 'blood_fbc', lambda x: BreastFormModel.blood_fbc.contains(x))
            query = restrict(query, filters, 'blood_fbc_report_id', lambda x: BreastFormModel.blood_fbc_report_id == x)
            query = restrict(query, filters, 'blood_lft_report_id', lambda x: BreastFormModel.blood_lft_report_id == x)
            query = restrict(query, filters, 'blood_urea_creatinine_report_id', lambda x: BreastFormModel.blood_urea_creatinine_report_id == x)
            query = restrict(query, filters, 'bone_scan_summary', lambda x: BreastFormModel.bone_scan_summary.contains(x))
            query = restrict(query, filters, 'stage_breast_location_id', lambda x: BreastFormModel.stage_breast_location_id == x)
            query = restrict(query, filters, 'stage_breast_t_id', lambda x: BreastFormModel.stage_breast_t_id == x)
            query = restrict(query, filters, 'stage_breast_n_id', lambda x: BreastFormModel.stage_breast_n_id == x)
            query = restrict(query, filters, 'stage_breast_m_id', lambda x: BreastFormModel.stage_breast_m_id == x)
            query = restrict(query, filters, 'user_create', lambda x: BreastFormModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: BreastFormModel.user_modify.contains(x))

        # default order
        query = query.order_by(BreastFormModel.id.desc())
        return paginated_results(query)
