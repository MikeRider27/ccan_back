import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.document_type import DocumentTypeModel
from utils import restrict, paginated_results
from security import check


class DocumentType(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('code', type=str)

    @jwt_required()
    @check('document_type_get')
    @swag_from('../swagger/document_type/get_document_type.yaml')
    def get(self, id):
        document_type = DocumentTypeModel.find_by_id(id)
        if document_type:
            return document_type.json()
        return {'message': _("DOCUMENT_TYPE_NOT_FOUND")}, 404

    @jwt_required()
    @check('document_type_update')
    @swag_from('../swagger/document_type/put_document_type.yaml')
    def put(self, id):
        document_type = DocumentTypeModel.find_by_id(id)
        if document_type:
            newdata = DocumentType.parser.parse_args()
            DocumentTypeModel.from_reqparse(document_type, newdata)
            document_type.save_to_db()
            return document_type.json()
        return {'message': _("DOCUMENT_TYPE_NOT_FOUND")}, 404

    @jwt_required()
    @check('document_type_delete')
    @swag_from('../swagger/document_type/delete_document_type.yaml')
    def delete(self, id):
        document_type = DocumentTypeModel.find_by_id(id)
        if document_type:
            document_type.delete_from_db()

        return {'message': _("DOCUMENT_TYPE_DELETED")}


class DocumentTypeList(Resource):

    @jwt_required()
    @check('document_type_list')
    @swag_from('../swagger/document_type/list_document_type.yaml')
    def get(self):
        query = DocumentTypeModel.query
        return paginated_results(query)

    @jwt_required()
    @check('document_type_insert')
    @swag_from('../swagger/document_type/post_document_type.yaml')
    def post(self):
        data = DocumentType.parser.parse_args()

        id = data.get('id')

        if id is not None and DocumentTypeModel.find_by_id(id):
            return {'message': _("DOCUMENT_TYPE_DUPLICATED").format(id)}, 400

        document_type = DocumentTypeModel(**data)
        try:
            document_type.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating document type.', exc_info=e)
            return {"message": _("DOCUMENT_TYPE_CREATE_ERROR")}, 500

        return document_type.json(), 201


class DocumentTypeSearch(Resource):

    @jwt_required()
    @check('document_type_search')
    @swag_from('../swagger/document_type/search_document_type.yaml')
    def post(self):
        query = DocumentTypeModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: DocumentTypeModel.id == x)
            query = restrict(query, filters, 'description', lambda x: func.lower(DocumentTypeModel.description).contains(func.lower(x)))
            query = restrict(query, filters, 'code', lambda x: DocumentTypeModel.code == x)

        return paginated_results(query)
