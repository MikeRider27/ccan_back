import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.periodicity import PeriodicityModel
from utils import restrict, paginated_results
from security import check


class Periodicity(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('active', type=bool)
    parser.add_argument('code', type=str)

    @jwt_required()
    @check('periodicity_get')
    @swag_from('../swagger/periodicity/get_periodicity.yaml')
    def get(self, id):
        periodicity = PeriodicityModel.find_by_id(id)
        if periodicity:
            return periodicity.json()
        return {'message': _("PERIODICITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('periodicity_update')
    @swag_from('../swagger/periodicity/put_periodicity.yaml')
    def put(self, id):
        periodicity = PeriodicityModel.find_by_id(id)
        if periodicity:
            newdata = Periodicity.parser.parse_args()
            PeriodicityModel.from_reqparse(periodicity, newdata)
            periodicity.save_to_db()
            return periodicity.json()
        return {'message': _("PERIODICITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('periodicity_delete')
    @swag_from('../swagger/periodicity/delete_periodicity.yaml')
    def delete(self, id):
        periodicity = PeriodicityModel.find_by_id(id)
        if periodicity:
            periodicity.delete_from_db()

        return {'message': _("PERIODICITY_DELETED")}


class PeriodicityList(Resource):

    @jwt_required()
    @check('periodicity_list')
    @swag_from('../swagger/periodicity/list_periodicity.yaml')
    def get(self):
        query = PeriodicityModel.query
        return paginated_results(query)

    @jwt_required()
    @check('periodicity_insert')
    @swag_from('../swagger/periodicity/post_periodicity.yaml')
    def post(self):
        data = Periodicity.parser.parse_args()

        id = data.get('id')

        if id is not None and PeriodicityModel.find_by_id(id):
            return {'message': _("PERIODICITY_DUPLICATED").format(id)}, 400

        periodicity = PeriodicityModel(**data)
        try:
            periodicity.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating periodicity.', exc_info=e)
            return {"message": _("PERIODICITY_CREATE_ERROR")}, 500

        return periodicity.json(), 201


class PeriodicitySearch(Resource):

    @jwt_required()
    @check('periodicity_search')
    @swag_from('../swagger/periodicity/search_periodicity.yaml')
    def post(self):
        query = PeriodicityModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PeriodicityModel.id == x)
            query = restrict(query, filters, 'description', lambda x: func.lower(PeriodicityModel.description).contains(func.lower(x)))
            query = restrict(query, filters, 'active', lambda x: x)
            query = restrict(query, filters, 'code', lambda x: func.lower(PeriodicityModel.code).contains(func.lower(x)))

        return paginated_results(query)
