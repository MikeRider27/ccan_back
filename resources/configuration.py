import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.configuration import ConfigurationModel
from utils import restrict, paginated_results
from security import check


class Configuration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('name', type=str)
    parser.add_argument('value', type=str)
    parser.add_argument('code', type=str)

    @jwt_required()
    @check('configuration_get')
    @swag_from('../swagger/configuration/get_configuration.yaml')
    def get(self, id):
        configuration = ConfigurationModel.find_by_id(id)
        if configuration:
            return configuration.json()
        return {'message': _("CONFIGURATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('configuration_update')
    @swag_from('../swagger/configuration/put_configuration.yaml')
    def put(self, id):
        configuration = ConfigurationModel.find_by_id(id)
        if configuration:
            newdata = Configuration.parser.parse_args()
            ConfigurationModel.from_reqparse(configuration, newdata)
            configuration.save_to_db()
            return configuration.json()
        return {'message': _("CONFIGURATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('configuration_delete')
    @swag_from('../swagger/configuration/delete_configuration.yaml')
    def delete(self, id):
        configuration = ConfigurationModel.find_by_id(id)
        if configuration:
            configuration.delete_from_db()

        return {'message': _("CONFIGURATION_DELETED")}


class ConfigurationList(Resource):

    @jwt_required()
    @check('configuration_list')
    @swag_from('../swagger/configuration/list_configuration.yaml')
    def get(self):
        query = ConfigurationModel.query
        return paginated_results(query)

    @jwt_required()
    @check('configuration_insert')
    @swag_from('../swagger/configuration/post_configuration.yaml')
    def post(self):
        data = Configuration.parser.parse_args()

        id = data.get('id')

        if id is not None and ConfigurationModel.find_by_id(id):
            return {'message': _("CONFIGURATION_DUPLICATED").format(id)}, 400

        configuration = ConfigurationModel(**data)
        try:
            configuration.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating configuration', exc_info=e)
            return {"message": _("CONFIGURATION_CREATE_ERROR")}, 500

        return configuration.json(), 201


class ConfigurationSearch(Resource):

    @jwt_required()
    @check('configuration_search')
    @swag_from('../swagger/configuration/search_configuration.yaml')
    def post(self):
        query = ConfigurationModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: ConfigurationModel.id == x)
            query = restrict(query, filters, 'name', lambda x: ConfigurationModel.name.contains(x))
            query = restrict(query, filters, 'value', lambda x: ConfigurationModel.value.contains(x))
            query = restrict(query, filters, 'code', lambda x: ConfigurationModel.code.contains(x))

        # default order
        query = query.order_by(ConfigurationModel.id.desc())
        return paginated_results(query)
