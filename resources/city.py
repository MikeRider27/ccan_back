import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import aliased
from flask_babel import _

from models.area import AreaModel
from models.city import CityModel
from utils import paginated_results, restrict_collector
from security import check


class City(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('area_id', type=int)

    @jwt_required()
    @check('city_get')
    @swag_from('../swagger/city/get_city.yaml')
    def get(self, id):
        city = CityModel.find_by_id(id)
        if city:
            return city.json()
        return {'message': _("CITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('city_update')
    @swag_from('../swagger/city/put_city.yaml')
    def put(self, id):
        city = CityModel.find_by_id(id)
        if city:
            newdata = City.parser.parse_args()
            CityModel.from_reqparse(city, newdata)
            city.save_to_db()
            return city.json()
        return {'message': _("CITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('city_delete')
    @swag_from('../swagger/city/delete_city.yaml')
    def delete(self, id):
        city = CityModel.find_by_id(id)
        if city:
            city.delete_from_db()

        return {'message': _("CITY_DELETED")}


class CityList(Resource):

    @jwt_required()
    @check('city_list')
    @swag_from('../swagger/city/list_city.yaml')
    def get(self):
        query = CityModel.query
        return paginated_results(query)

    @jwt_required()
    @check('city_insert')
    @swag_from('../swagger/city/post_city.yaml')
    def post(self):
        data = City.parser.parse_args()

        id = data.get('id')

        if id is not None and CityModel.find_by_id(id):
            return {'message': _("CITY_DUPLICATED").format(id)}, 400

        city = CityModel(**data)
        try:
            city.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating city', exc_info=e)
            return {"message": _("CITY_CREATE_ERROR")}, 500

        return city.json(), 201


class CitySearch(Resource):

    @jwt_required()
    @check('city_search')
    @swag_from('../swagger/city/search_city.yaml')
    def post(self):
        query = CityModel.query

        # Relationship
        area = aliased(AreaModel)
        query = query.join(area, CityModel.area_id == area.id, isouter=True)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: CityModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'area_id', lambda x: CityModel.area_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'description', lambda x: func.lower(CityModel.description).contains(func.lower(x)))

            # Relationship Filter
            or_filter_list = restrict_collector(or_filter_list, filters, 'area',
                             lambda x: func.lower(area.description).contains(func.lower(x)))

            # Apply filters
            general_filter = request.args.get('general_filter', None, str) == 'true'
            if general_filter:
                query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
            else:
                filter_list = and_filter_list + or_filter_list
                query = query.filter(and_(*filter_list))

        return paginated_results(query)
