import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy import and_, or_, func, cast, String

from dao.medical_documents_dao import MedicalDocumentsDao
from models.medical_document_type import MedicalDocumentTypeModel
from models.patient_exclusion_criteria import PatientExclusionCriteriaModel
from models.patient_inclusion_criteria import PatientInclusionCriteriaModel
from models.patient_inclusion_criteria_adjuvant_trastuzumab import PatientInclusionCriteriaAdjuvantTrastuzumabModel
from models.patient_inclusion_criteria_neoadjuvant_trastuzumab import \
    PatientInclusionCriteriaNeoadjuvantTrastuzumabModel
from security import check
from utils import restrict, paginated_results, restrict_collector


class MedicalDocumentType(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('orden', type=int)
    parser.add_argument('code', type=str)
    parser.add_argument('active', type=bool)

    @jwt_required()
    @check('medical_document_type_get')
    @swag_from('../swagger/medical_document_type/get_medical_document_type.yaml')
    def get(self, id):
        medical_document_type = MedicalDocumentTypeModel.find_by_id(id)
        if medical_document_type:
            return medical_document_type.json()
        return {'message': _("MEDICAL_DOCUMENT_TYPE_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_document_type_update')
    @swag_from('../swagger/medical_document_type/put_medical_document_type.yaml')
    def put(self, id):
        medical_document_type = MedicalDocumentTypeModel.find_by_id(id)
        if medical_document_type:
            newdata = MedicalDocumentType.parser.parse_args()
            MedicalDocumentTypeModel.from_reqparse(medical_document_type, newdata)
            medical_document_type.save_to_db()
            return medical_document_type.json()
        return {'message': _("MEDICAL_DOCUMENT_TYPE_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_document_type_delete')
    @swag_from('../swagger/medical_document_type/delete_medical_document_type.yaml')
    def delete(self, id):
        medical_document_type = MedicalDocumentTypeModel.find_by_id(id)
        if medical_document_type:
            medical_document_type.delete_from_db()

        return {'message': _("MEDICAL_DOCUMENT_TYPE_DELETED")}


class MedicalDocumentTypeList(Resource):

    @jwt_required()
    @check('medical_document_type_list')
    @swag_from('../swagger/medical_document_type/list_medical_document_type.yaml')
    def get(self):
        query = MedicalDocumentTypeModel.query
        query = query.filter(MedicalDocumentTypeModel.active == True)
        return paginated_results(query)

    @jwt_required()
    @check('medical_document_type_insert')
    @swag_from('../swagger/medical_document_type/post_medical_document_type.yaml')
    def post(self):
        data = MedicalDocumentType.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicalDocumentTypeModel.find_by_id(id):
            return {'message': _("MEDICAL_DOCUMENT_TYPE_DUPLICATED").format(id)}, 400

        medical_document_type = MedicalDocumentTypeModel(**data)
        try:
            medical_document_type.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating medical document type.', exc_info=e)
            return {"message": _("MEDICAL_DOCUMENT_TYPE_CREATE_ERROR")}, 500

        return medical_document_type.json(), 201


class MedicalDocumentTypeSearch(Resource):

    @jwt_required()
    @check('medical_document_type_search')
    @swag_from('../swagger/medical_document_type/search_medical_document_type.yaml')
    def post(self):
        query = MedicalDocumentTypeModel.query

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json

            or_filter_list = restrict_collector(or_filter_list, filters, 'active', lambda x: MedicalDocumentTypeModel.active == (x.lower() == 'si') if x.lower() in ['si', 'no'] else None)
            or_filter_list = restrict_collector(or_filter_list, filters, 'description', lambda x: func.lower(MedicalDocumentTypeModel.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'orden', lambda x: cast(MedicalDocumentTypeModel.orden,String).contains(str(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(MedicalDocumentTypeModel.code).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        # default order
        query = query.order_by(MedicalDocumentTypeModel.id.asc())

        return paginated_results(query)


class MedicalDocumentTypeInitialList(Resource):
    @jwt_required()
    @check('medical_document_type_list')
    @swag_from('../swagger/medical_document_type/list_medical_document_type_initial.yaml')
    def get(self):
        query = MedicalDocumentTypeModel.query
        query = query.filter(MedicalDocumentTypeModel.description == 'INITIAL_PATIENT_DOCUMENTS')
        return paginated_results(query)


class MedicalDocumentTypeRequirementsList(Resource):
    @jwt_required()
    @check('medical_document_type_list')
    @swag_from('../swagger/medical_document_type/list_medical_document_type_requirements.yaml')
    def get(self, patient_id):
        medical_documents_dao = MedicalDocumentsDao()
        type_list = medical_documents_dao.get_requirements_files_data(patient_id=patient_id)

        for type in type_list:
            if type.get('type_code', None) == 'INCL_FORM':
                # Inclusion Criteria
                inclusion_form = None
                patientInclusionCriteriaModel = PatientInclusionCriteriaModel.query.filter_by(
                    patient_id=patient_id).order_by(
                    PatientInclusionCriteriaModel.date_create.desc()).first()
                if patientInclusionCriteriaModel:
                    if patientInclusionCriteriaModel.patient_inclusion_criteria_adjuvant_id:
                        id = patientInclusionCriteriaModel.patient_inclusion_criteria_adjuvant_id
                        inclusion_form = PatientInclusionCriteriaAdjuvantTrastuzumabModel.find_by_id(id)
                    elif patientInclusionCriteriaModel.patient_inclusion_criteria_neoadjuvant_id:
                        id = patientInclusionCriteriaModel.patient_inclusion_criteria_neoadjuvant_id
                        inclusion_form = PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.find_by_id(id)

                if not inclusion_form and not type.get('id', None):
                    type['type_description'] += f' ({_("INCL_DOCUMENT_FORM_MISSING")})'
                else:
                    if not inclusion_form and type.get('id', None):
                        type['type_description'] += f' ({_("INCL_FORM_MISSING")})'
                    if inclusion_form and not type.get('id', None):
                        type['type_description'] += f' ({_("DOCUMENT_MISSING")})'

                # Se asigna el valor de completado
                # Si se completo el formulario y se ha adjuntado el documento fisico
                if type.get('id', None) is not None and inclusion_form is not None:
                    if patientInclusionCriteriaModel.patient_inclusion_criteria_neoadjuvant_id:
                        type['complete'] = inclusion_form.patient_included()
                        if not type['complete']:
                            doc_en_falta = inclusion_form.get_documentos_faltantes()
                            if len(doc_en_falta) > 0:
                                type['type_description'] += f" ({_('INCL_CRITERIA_FAIL')}. {', '.join(doc_en_falta)})"
                            else:
                                type['type_description'] += f' ({_("INCL_CRITERIA_FAIL")})'
                    else:
                        type['complete'] = True
                else:
                    type['complete'] = False

            elif type.get('type_code', None) == 'EXCL_FORM':
                # Exclusion criteria
                exclusion_form = PatientExclusionCriteriaModel.query.filter_by(patient_id=patient_id).order_by(
                    PatientExclusionCriteriaModel.date_create.desc()).first()

                if not exclusion_form and not type.get('id', None):
                    type['type_description'] += f' ({_("EXCL_DOCUMENT_FORM_MISSING")})'
                else:
                    if not exclusion_form and type.get('id', None):
                        type['type_description'] += f' ({_("EXCL_FORM_MISSING")})'
                    if exclusion_form and not type.get('id', None):
                        type['type_description'] += f' ({_("DOCUMENT_MISSING")})'

                # Se asigna el Valor de completado
                type['complete'] = type.get('id', None) is not None and exclusion_form is not None

            else:
                type['complete'] = type.get('id', None) is not None

        return type_list, 200
