import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy.orm import aliased
from flask_babel import _

from models.area import AreaModel
from models.country import CountryModel
from utils import paginated_results, restrict_collector
from security import check
from sqlalchemy import and_, or_, func


class Area(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('country_id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('area_number', type=int)

    @jwt_required()
    @check('area_get')
    @swag_from('../swagger/area/get_area.yaml')
    def get(self, id):
        area = AreaModel.find_by_id(id)
        if area:
            return area.json()
        return {'message': _("AREA_NOT_FOUND")}, 404

    @jwt_required()
    @check('area_update')
    @swag_from('../swagger/area/put_area.yaml')
    def put(self, id):
        area = AreaModel.find_by_id(id)
        if area:
            newdata = Area.parser.parse_args()
            AreaModel.from_reqparse(area, newdata)
            area.save_to_db()
            return area.json()
        return {'message': _("AREA_NOT_FOUND")}, 404

    @jwt_required()
    @check('area_delete')
    @swag_from('../swagger/area/delete_area.yaml')
    def delete(self, id):
        area = AreaModel.find_by_id(id)
        if area:
            area.delete_from_db()

        return {'message': _("AREA_DELETED")}


class AreaList(Resource):

    @jwt_required()
    @check('area_list')
    @swag_from('../swagger/area/list_area.yaml')
    def get(self):
        query = AreaModel.query
        return paginated_results(query)

    @jwt_required()
    @check('area_insert')
    @swag_from('../swagger/area/post_area.yaml')
    def post(self):
        data = Area.parser.parse_args()

        id = data.get('id')

        if id is not None and AreaModel.find_by_id(id):
            return {'message': _("AREA_DUPLICATED").format(id)}, 400

        area = AreaModel(**data)
        try:
            area.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating area.', exc_info=e)
            return {"message": _("AREA_CREATE_ERROR")}, 500

        return area.json(), 201


class AreaSearch(Resource):

    @jwt_required()
    @check('area_search')
    @swag_from('../swagger/area/search_area.yaml')
    def post(self):
        query = AreaModel.query

        # Relationship
        country = aliased(CountryModel)
        query = query.join(country, AreaModel.country_id == country.id, isouter=True)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: AreaModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'country_id', lambda x: AreaModel.country_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'description', lambda x: func.lower(AreaModel.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'area_number', lambda x: AreaModel.area_number == x)

            # Relationship Filter
            or_filter_list = restrict_collector(or_filter_list, filters, 'country',
                                                lambda x: func.lower(country.description).contains(func.lower(x)))

        # Apply filters
        general_filter = request.args.get('general_filter', None, str) == 'true'
        if general_filter:
            query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
        else:
            filter_list = and_filter_list + or_filter_list
            query = query.filter(and_(*filter_list))

        return paginated_results(query)
    
        
