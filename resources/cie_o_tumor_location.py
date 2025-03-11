import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy.sql import func, and_, or_
from sqlalchemy.orm import aliased

from db import db
from models.cie_o_topography import CieOTopographyModel
from models.cie_o_tumor_location import CieOTumorLocationModel
from security import check
from utils import restrict, paginated_results, restrict_collector
from security import check


class CieOTumorLocation(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('code', type=str)
    parser.add_argument('description_es', type=str)
    parser.add_argument('description_en', type=str)
    parser.add_argument('cie_o_topography_id', type=int)

    @jwt_required()
    @check('cie_o_tumor_location_get')
    @swag_from('../swagger/cie_o_tumor_location/get_cie_o_tumor_location.yaml')
    def get(self, id):
        cie_o = CieOTumorLocationModel.find_by_id(id)
        if cie_o:
            return cie_o.json()
        return {'message': _("CIEOTL_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_o_tumor_location_update')
    @swag_from('../swagger/cie_o_tumor_location/put_cie_o_tumor_location.yaml')
    def put(self, id):
        cie_o = CieOTumorLocationModel.find_by_id(id)
        if cie_o:
            newdata = CieOTumorLocation.parser.parse_args()
            CieOTumorLocationModel.from_reqparse(cie_o, newdata)
            cie_o.save_to_db()
            return cie_o.json()
        return {'message': _("CIEOTL_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_o_tumor_location_delete')
    @swag_from('../swagger/cie_o_tumor_location/delete_cie_o_tumor_location.yaml')
    def delete(self, id):
        cie_o = CieOTumorLocationModel.find_by_id(id)
        if cie_o:
            cie_o.delete_from_db()

        return {'message': _("CIEOTL_DELETED")}


class CieOTumorLocationList(Resource):

    @jwt_required()
    @check('cie_o_tumor_location_list')
    @swag_from('../swagger/cie_o_tumor_location/list_cie_o_tumor_location.yaml')
    def get(self):
        query = CieOTumorLocationModel.query
        return paginated_results(query)

    @jwt_required()
    @check('cie_o_tumor_location_insert')
    @swag_from('../swagger/cie_o_tumor_location/post_cie_o_tumor_location.yaml')
    def post(self):
        data = CieOTumorLocation.parser.parse_args()

        id = data.get('id')

        if id is not None and CieOTumorLocationModel.find_by_id(id):
            return {'message': _("CIEOTL_DUPLICATED").format(id)}, 400

        cie_o = CieOTumorLocationModel(**data)
        try:
            cie_o.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating CIE-O Tumor Location.', exc_info=e)
            return {"message": _("CIEOTL_CREATE_ERROR")}, 500

        return cie_o.json(), 201


class CieOTumorLocationSearch(Resource):

    @jwt_required()
    @check('cie_o_tumor_location_search')
    @swag_from('../swagger/cie_o_tumor_location/search_cie_o_tumor_location.yaml')
    def post(self):
        query = CieOTumorLocationModel.query

        and_filter_list = []
        or_filter_list = []
        cie_o_topography = aliased(CieOTopographyModel)
        query = query.outerjoin(cie_o_topography, CieOTumorLocationModel.cie_o_topography_id == cie_o_topography.id)
        if request.json:
            filters = request.json
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(CieOTumorLocationModel.code).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description_es',
                                                lambda x: func.lower(CieOTumorLocationModel.description_es).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description_en',
                                                lambda x: func.lower(CieOTumorLocationModel.description_en).contains(func.lower(x)))

            or_filter_list = restrict_collector(or_filter_list, filters, 'cie_o_topography',
                                                lambda x: func.lower(cie_o_topography.description_es).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
        return paginated_results(query)
