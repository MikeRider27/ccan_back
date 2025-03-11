import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import and_, or_, func
from flask_babel import _

from models.cie_o_morphology import CieOMorphologyModel
from security import check
from utils import paginated_results, restrict_collector


class CieOMorphology(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('code', type=str)
    parser.add_argument('description_en', type=str)
    parser.add_argument('desription_es', type=str)

    @jwt_required()
    @check('cie_o_morphology_get')
    @swag_from('../swagger/cie_o_morphology/get_cie_o_morphology.yaml')
    def get(self, id):
        cie_o = CieOMorphologyModel.find_by_id(id)
        if cie_o:
            return cie_o.json()
        return {'message': _("CIEOM_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_o_morphology_update')
    @swag_from('../swagger/cie_o_morphology/put_cie_o_morphology.yaml')
    def put(self, id):
        cie_o = CieOMorphologyModel.find_by_id(id)
        if cie_o:
            newdata = CieOMorphology.parser.parse_args()
            CieOMorphologyModel.from_reqparse(cie_o, newdata)
            cie_o.save_to_db()
            return cie_o.json()
        return {'message': _("CIEOM_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_o_morphology_delete')
    @swag_from('../swagger/cie_o_morphology/delete_cie_o_morphology.yaml')
    def delete(self, id):
        cie_o = CieOMorphologyModel.find_by_id(id)
        if cie_o:
            cie_o.delete_from_db()

        return {'message':  _("CIEOM_DELETED")}


class CieOMorphologyList(Resource):

    @jwt_required()
    @check('cie_o_morphology_list')
    @swag_from('../swagger/cie_o_morphology/list_cie_o_morphology.yaml')
    def get(self):
        query = CieOMorphologyModel.query
        return paginated_results(query)

    @jwt_required()
    @check('cie_o_morphology_insert')
    @swag_from('../swagger/cie_o_morphology/post_cie_o_morphology.yaml')
    def post(self):
        data = CieOMorphology.parser.parse_args()

        id = data.get('id')

        if id is not None and CieOMorphologyModel.find_by_id(id):
            return {'message': _("CIEOM_DUPLICATED").format(id)}, 400

        cie_o = CieOMorphologyModel(**data)
        try:
            cie_o.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating CIE-O Morphology.', exc_info=e)
            return {"message": _("CIEOM_CREATE_ERROR")}, 500

        return cie_o.json(), 201


class CieOMorphologySearch(Resource):

    @jwt_required()
    @check('cie_o_morphology_search')
    @swag_from('../swagger/cie_o_morphology/search_cie_o_morphology.yaml')
    def post(self):
        query = CieOMorphologyModel.query

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: CieOMorphologyModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'term_es', lambda x: func.lower(CieOMorphologyModel.term_es).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'term_en', lambda x: func.lower(CieOMorphologyModel.term_en).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(CieOMorphologyModel.code).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
