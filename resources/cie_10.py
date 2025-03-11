import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import and_, or_, func
from flask_babel import _

from models.cie_10 import Cie_10Model
from security import check
from utils import paginated_results, restrict_collector
from security import check


class Cie_10(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('code', type=str)
    parser.add_argument('description_es', type=str)
    parser.add_argument('description_en', type=str)

    @jwt_required()
    @check('cie_10_get')
    @swag_from('../swagger/cie_10/get_cie_10.yaml')
    def get(self, id):
        cie_10 = Cie_10Model.find_by_id(id)
        if cie_10:
            return cie_10.json()
        return {'message': _("CIE10_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_10_update')
    @swag_from('../swagger/cie_10/put_cie_10.yaml')
    def put(self, id):
        cie_10 = Cie_10Model.find_by_id(id)
        if cie_10:
            newdata = Cie_10.parser.parse_args()
            Cie_10Model.from_reqparse(cie_10, newdata)
            cie_10.save_to_db()
            return cie_10.json()
        return {'message': _("CIE10_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_10_delete')
    @swag_from('../swagger/cie_10/delete_cie_10.yaml')
    def delete(self, id):
        cie_10 = Cie_10Model.find_by_id(id)
        if cie_10:
            cie_10.delete_from_db()

        return {'message': _("CIE10_DELETED")}


class Cie_10List(Resource):

    @jwt_required()
    @check('cie_10_list')
    @swag_from('../swagger/cie_10/list_cie_10.yaml')
    def get(self):
        query = Cie_10Model.query
        return paginated_results(query)

    @jwt_required()
    @check('cie_10_insert')
    @swag_from('../swagger/cie_10/post_cie_10.yaml')
    def post(self):
        data = Cie_10.parser.parse_args()

        id = data.get('id')

        if id is not None and Cie_10Model.find_by_id(id):
            return {'message': _("CIE10_DUPLICATED").format(id)}, 400

        cie_10 = Cie_10Model(**data)
        try:
            cie_10.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating CIE10.', exc_info=e)
            return {"message": _("CIE10_CREATE_ERROR")}, 500

        return cie_10.json(), 201


class Cie_10Search(Resource):

    @jwt_required()
    @check('cie_10_search')
    @swag_from('../swagger/cie_10/search_cie_10.yaml')
    def post(self):
        query = Cie_10Model.query

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: Cie_10Model.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(Cie_10Model.code).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description_es', lambda x: func.lower(Cie_10Model.description_es).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description_en', lambda x: func.lower(Cie_10Model.description_en).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
