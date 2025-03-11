import logging

from flasgger import swag_from
from flask import request
from flask_babel import _
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.parameter import ParameterModel
from security import check
from utils import paginated_results, restrict_collector, restrict
from sqlalchemy import and_, or_, func

class Parameter(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('domain', type=str)
    parser.add_argument('value', type=str)
    parser.add_argument('active', type=bool)
    parser.add_argument('code', type=str)

    @jwt_required()
    @check('parameter_get')
    @swag_from('../swagger/parameter/get_parameter.yaml')
    def get(self, id):
        parameter = ParameterModel.find_by_id(id)
        if parameter:
            return parameter.json()
        return {'message': _("PARAMETER_NOT_FOUND")}, 404

    @jwt_required()
    @check('parameter_update')
    @swag_from('../swagger/parameter/put_parameter.yaml')
    def put(self, id):
        parameter = ParameterModel.find_by_id(id)
        if parameter:
            newdata = Parameter.parser.parse_args()
            ParameterModel.from_reqparse(parameter, newdata)
            parameter.save_to_db()
            return parameter.json()
        return {'message': _("PARAMETER_NOT_FOUND")}, 404

    @jwt_required()
    @check('parameter_delete')
    @swag_from('../swagger/parameter/delete_parameter.yaml')
    def delete(self, id):
        parameter = ParameterModel.find_by_id(id)
        if parameter:
            parameter.delete_from_db()

        return {'message': _("PARAMETER_DELETED")}


class ParameterList(Resource):

    @jwt_required()
    @check('parameter_list')
    @swag_from('../swagger/parameter/list_parameter.yaml')
    def get(self):
        query = ParameterModel.query
        return paginated_results(query)

    @jwt_required()
    @check('parameter_insert')
    @swag_from('../swagger/parameter/post_parameter.yaml')
    def post(self):
        data = Parameter.parser.parse_args()

        id = data.get('id')

        if id is not None and ParameterModel.find_by_id(id):
            return {'message': _("PARAMETER_DUPLICATED").format(id)}, 400

        parameter = ParameterModel(**data)
        try:
            parameter.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating parameter.', exc_info=e)
            return {"message": _("PARAMETER_CREATE_ERROR")}, 500

        return parameter.json(), 201


class ParameterSearch(Resource):
    @jwt_required()
    @check('parameter_search')
    @swag_from('../swagger/parameter/search_parameter.yaml')
    def post(self):
        query = ParameterModel.query

        # Preprocessing
        filters = request.json
        or_filter = filters.get('or_filter', False) or False
        if or_filter:
            if 'active' in filters:
                if filters['active']:
                    value = filters['active'].lower()
                    if value in ['si', 'sí']:
                        filters['active'] = True
                    elif value in ['no']:
                        filters['active'] = False
                    else:
                        # Se elimina para no evaluar
                        del filters['active']

        and_filter_list = []
        or_filter_list = []
        if filters:
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: ParameterModel.id == x)

            if or_filter:
                or_filter_list = restrict_collector(or_filter_list, filters, 'active', lambda x: ParameterModel.active == x)
                or_filter_list = restrict_collector(or_filter_list, filters, 'domain', lambda x: func.lower(ParameterModel.domain).contains(func.lower(x)))
                or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(ParameterModel.code).contains(func.lower(x)))
            else:
                and_filter_list = restrict_collector(and_filter_list, filters, 'active', lambda x: ParameterModel.active == x)
                and_filter_list = restrict_collector(and_filter_list, filters, 'domain', lambda x: func.lower(ParameterModel.domain) == func.lower(x))
                and_filter_list = restrict_collector(and_filter_list, filters, 'code', lambda x: func.lower(ParameterModel.code) == func.lower(x))

            or_filter_list = restrict_collector(or_filter_list, filters, 'value', lambda x: func.lower(ParameterModel.value).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        # default order
        query = query.order_by(ParameterModel.id.asc())

        return paginated_results(query)
