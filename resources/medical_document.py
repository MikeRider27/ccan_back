import json
import logging
import os
import traceback
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename
from flask_babel import _

from db import db
from models.medical_document import MedicalDocumentModel
from models.medical_document_type import MedicalDocumentTypeModel
from resources.patient import patient_update_state
from utils import restrict, paginated_results, get_file_directory, get_filename_hash, check_length_path, delete_file, \
    restrict_collector
from security import check


MODULE = 'patient_medical_documents'


class MedicalDocument(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('path', type=str)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('medical_document_type_id', type=int)
    parser.add_argument('modulo', type=str)
    parser.add_argument('origen_id', type=int)
    parser.add_argument('study_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y') if x else None)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('hospital_id', type=int)

    @jwt_required()
    @check('medical_document_get')
    @swag_from('../swagger/medical_document/get_medical_document.yaml')
    def get(self, id):
        medical_document = MedicalDocumentModel.find_by_id(id)
        if medical_document:
            return medical_document.json()
        return {'message': _("MEDICAL_DOCUMENT_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_document_update')
    @swag_from('../swagger/medical_document/put_medical_document.yaml')
    def put(self, id):
        medical_document = MedicalDocumentModel.find_by_id(id)
        if medical_document:
            newdata = MedicalDocument.parser.parse_args()
            MedicalDocumentModel.from_reqparse(medical_document, newdata)

            medical_document.user_modify = get_jwt_identity()
            medical_document.date_modify = datetime.now()
            medical_document.save_to_db()
            return medical_document.json()
        return {'message': _("MEDICAL_DOCUMENT_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_document_delete')
    @swag_from('../swagger/medical_document/delete_medical_document.yaml')
    def delete(self, id):
        medical_document = MedicalDocumentModel.find_by_id(id)
        if medical_document:
            medical_document.delete_from_db()

        return {'message': _("MEDICAL_DOCUMENT_DELETED")}


class MedicalDocumentList(Resource):

    @jwt_required()
    @check('medical_document_list')
    @swag_from('../swagger/medical_document/list_medical_document.yaml')
    def get(self):
        query = MedicalDocumentModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medical_document_insert')
    @swag_from('../swagger/medical_document/post_medical_document.yaml')
    def post(self):
        # Documents list
        files = request.files

        # data to save
        data = json.loads(request.form.to_dict()['dataSerialize'] if 'dataSerialize' in request.form else None)

        id = data.get('id')

        if id is not None and MedicalDocumentModel.find_by_id(id):
            return {'message': _("MEDICAL_DOCUMENT_DUPLICATED").format(id)}, 400

        filepath_list = []
        try:
            with db.session.no_autoflush:
                file = files['file']
                del data['file']
                data['id'] = None
                data['path'] = persist_document(file)
                filepath_list.append(data['path'])
                if 'study_date' in data and data['study_date']:
                    data['study_date'] = datetime.strptime(data['study_date'], '%d/%m/%Y')
                medical_document_model = MedicalDocumentModel(**data)
                medical_document_model.user_create = get_jwt_identity()
                db.session.add(medical_document_model)

                # Se persisiten todos los cambios
                db.session.commit()

                # LLamar evento de cambio de estado de paciente
                patient_update_state(data.get('patient_id', None))
        except Exception as e:
            # Se revierte los cambios
            db.session.rollback()

            # printing stack trace
            traceback.print_exc()

            # Eliminar archivos que pudieran haber sido persisitidos
            for filepath in filepath_list:
                delete_file(filepath)

            logging.error('An error occurred while creating medical document.', exc_info=e)
            return {"message": _("MEDICAL_DOCUMENT_CREATE_ERROR")}, 500

        return {'message': _("MEDICAL_DOCUMENT_SAVED")}, 201


class MedicalDocumentSearch(Resource):

    @jwt_required()
    @check('medical_document_search')
    @swag_from('../swagger/medical_document/search_medical_document.yaml')
    def post(self):
        query = MedicalDocumentModel.query
        document_type = aliased(MedicalDocumentTypeModel)
        query = query.join(document_type, MedicalDocumentModel.medical_document_type_id == document_type.id)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'patient_id', lambda x: MedicalDocumentModel.patient_id == x)
            and_filter_list = restrict_collector(and_filter_list, filters, 'modulo', lambda x: func.lower(MedicalDocumentModel.modulo).contains(func.lower(x)))
            # query = restrict(query, filters, 'id', lambda x: MedicalDocumentModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'description', lambda x: func.lower(MedicalDocumentModel.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'medical_document_type', lambda x: func.lower(document_type.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'modulo', lambda x: func.lower(MedicalDocumentModel.modulo).contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'origen_id', lambda x: MedicalDocumentModel.origen_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'study_date', lambda x: func.to_char(MedicalDocumentModel.study_date, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict(or_filter_list, filters, 'date_create',
                             lambda x: func.to_char(MedicalDocumentModel.date_create, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict(or_filter_list, filters, 'user_create', lambda x: MedicalDocumentModel.user_create.contains(x))
            or_filter_list = restrict(or_filter_list, filters, 'date_modify',
                             lambda x: func.to_char(MedicalDocumentModel.date_modify, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict(or_filter_list, filters, 'user_modify', lambda x: MedicalDocumentModel.user_modify.contains(x))

            # Apply filters
            general_filter = request.args.get('general_filter', None, str) == 'true'
            if general_filter:
                query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
            else:
                filter_list = and_filter_list + or_filter_list
                query = query.filter(and_(*filter_list))

        return paginated_results(query)


def persist_document(file, module=None):
    try:
        # Persist file
        if not module:
            module = MODULE
        path_string = get_file_directory(module)
        filename = secure_filename(file.filename)
        filename_hash = get_filename_hash(filename)
        path = os.path.join(path_string, filename_hash)
        path = check_length_path(path)
        file.save(path)
        return path
    except Exception as e:
        logging.error(_("MEDICAL_DOCUMENT_PERSIST_ERROR"), exc_info=e)


class MedicalDocumentInitialSearch(Resource):
    @jwt_required()
    @check('medical_document_list')
    @swag_from('../swagger/medical_document/search_medical_document_initial.yaml')
    def post(self):
        query = MedicalDocumentModel.query
        document_type = aliased(MedicalDocumentTypeModel)
        query = query.join(document_type, and_(MedicalDocumentModel.medical_document_type_id == document_type.id,
                                               document_type.description == 'INITIAL_PATIENT_DOCUMENTS'))

        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MedicalDocumentModel.id == x)
            query = restrict(query, filters, 'title', lambda x: func.lower(MedicalDocumentModel.title).contains(x))
            query = restrict(query, filters, 'description', lambda x: MedicalDocumentModel.description.contains(x))
            query = restrict(query, filters, 'path', lambda x: MedicalDocumentModel.path.contains(x))
            query = restrict(query, filters, 'patient_id', lambda x: MedicalDocumentModel.patient_id == x)
            query = restrict(query, filters, 'medical_document_type_id', lambda x: MedicalDocumentModel.medical_document_type_id == x)
            query = restrict(query, filters, 'modulo', lambda x: func.lower(MedicalDocumentModel.modulo).contains(x))
            query = restrict(query, filters, 'origen_id', lambda x: MedicalDocumentModel.origen_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: MedicalDocumentModel.hospital_id == x)
        return paginated_results(query)
