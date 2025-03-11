import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import aliased

from models.cie_o_topography import CieOTopographyModel
from models.gender import GenderModel
from security import check
from utils import restrict, paginated_results, restrict_collector
from security import check


class CieOTopography(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('code', type=str)
    parser.add_argument('description_es', type=str)
    parser.add_argument('description_en', type=str)
    parser.add_argument('gender_id', type=int)

    @jwt_required()
    @check('cie_o_topography_get')
    @swag_from('../swagger/cie_o_topography/get_cie_o_topography.yaml')
    def get(self, id):
        cie_o = CieOTopographyModel.find_by_id(id)
        if cie_o:
            return cie_o.json()
        return {'message': _("CIEOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_o_topography_update')
    @swag_from('../swagger/cie_o_topography/put_cie_o_topography.yaml')
    def put(self, id):
        cie_o = CieOTopographyModel.find_by_id(id)
        if cie_o:
            newdata = CieOTopography.parser.parse_args()
            CieOTopographyModel.from_reqparse(cie_o, newdata)
            cie_o.save_to_db()
            return cie_o.json()
        return {'message': _("CIEOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('cie_o_topography_delete')
    @swag_from('../swagger/cie_o_topography/delete_cie_o_topography.yaml')
    def delete(self, id):
        cie_o = CieOTopographyModel.find_by_id(id)
        if cie_o:
            cie_o.delete_from_db()

        return {'message': _("CIEOT_DELETED")}


class CieOTopographyList(Resource):

    @jwt_required()
    @check('cie_o_topography_list')
    @swag_from('../swagger/cie_o_topography/list_cie_o_topography.yaml')
    def get(self):
        query = CieOTopographyModel.query
        return paginated_results(query)

    @jwt_required()
    @check('cie_o_topography_insert')
    @swag_from('../swagger/cie_o_topography/post_cie_o_topography.yaml')
    def post(self):
        data = CieOTopography.parser.parse_args()

        id = data.get('id')

        if id is not None and CieOTopographyModel.find_by_id(id):
            return {'message': _("CIEOT_DUPLICATED").format(id)}, 400

        cie_o = CieOTopographyModel(**data)
        try:
            cie_o.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating CIE-O Topografia.', exc_info=e)
            return {"message": _("CIEOT_CREATE_ERROR")}, 500

        return cie_o.json(), 201


class CieOTopographySearch(Resource):

    @jwt_required()
    @check('cie_o_topography_search')
    @swag_from('../swagger/cie_o_topography/search_cie_o_topography.yaml')
    def post(self):
        query = CieOTopographyModel.query

        # gender = GenderModel.query.filter_by(id=CieOTopographyModel.gender_id).first()
        gender = aliased(GenderModel)
        query = query.outerjoin(gender, CieOTopographyModel.gender_id == gender.id)
        and_filter_list = []
        or_filter_list = []

        if request.json:
            filters = request.json
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(CieOTopographyModel.code).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description_es', lambda x: func.lower(CieOTopographyModel.description_es).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description_en', lambda x: func.lower(CieOTopographyModel.description_en).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'gender', lambda x: func.lower(gender.description).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
