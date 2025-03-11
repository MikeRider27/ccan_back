import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import and_, or_, func
from flask_babel import _

from models.country import CountryModel
from utils import paginated_results, restrict_collector

from security import check

class Country(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('code', type=str)
    parser.add_argument('nationality', type=str)

    @jwt_required()
    @check('country_get')
    @swag_from('../swagger/country/get_country.yaml')
    def get(self, id):
        country = CountryModel.find_by_id(id)
        if country:
            return country.json()
        return {'message': _("COUNTRY_NOT_FOUND")}, 404

    @jwt_required()
    @check('country_update')
    @swag_from('../swagger/country/put_country.yaml')
    def put(self, id):
        country = CountryModel.find_by_id(id)
        if country:
            newdata = Country.parser.parse_args()
            CountryModel.from_reqparse(country, newdata)
            country.save_to_db()
            return country.json()
        return {'message': _("COUNTRY_NOT_FOUND")}, 404

    @jwt_required()
    @check('country_delete')
    @swag_from('../swagger/country/delete_country.yaml')
    def delete(self, id):
        country = CountryModel.find_by_id(id)
        if country:
            country.delete_from_db()

        return {'message': _("COUNTRY_DELETED")}


class CountryList(Resource):

    @jwt_required()
    @check('country_list')
    @swag_from('../swagger/country/list_country.yaml')
    def get(self):
        query = CountryModel.query
        return paginated_results(query)

    @jwt_required()
    @check('country_insert')
    @swag_from('../swagger/country/post_country.yaml')
    def post(self):
        data = Country.parser.parse_args()

        id = data.get('id')

        if id is not None and CountryModel.find_by_id(id):
            return {'message': _("COUNTRY_DUPLICATED").format(id)}, 400

        country = CountryModel(**data)
        try:
            country.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating country.', exc_info=e)
            return {"message": _("COUNTRY_CREATE_ERROR")}, 500

        return country.json(), 201


class CountrySearch(Resource):

    @jwt_required()
    @check('country_search')
    @swag_from('../swagger/country/search_country.yaml')
    def post(self):
        query = CountryModel.query
        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: CountryModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(CountryModel.code).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description', lambda x: func.lower(CountryModel.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'nationality', lambda x: func.lower(CountryModel.nationality).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
