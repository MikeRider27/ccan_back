import base64
import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.module_role import ModuleRoleModel
from utils import restrict, paginated_results
from security import check


class ModuleRole(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('module_id', type=int)
    parser.add_argument('role_id', type=int)

    @jwt_required()
    @check('module_role_get')
    @swag_from('../swagger/module_role/get_module_role.yaml')
    def get(self, id):
        module_role = ModuleRoleModel.find_by_id(id)
        if module_role:
            return module_role.json()
        return {'message': 'No se encuentra Module_role'}, 404

    @jwt_required()
    @check('module_role_update')
    @swag_from('../swagger/module_role/put_module_role.yaml')
    def put(self, id):
        module_role = ModuleRoleModel.find_by_id(id)
        if module_role:
            newdata = ModuleRole.parser.parse_args()
            ModuleRoleModel.from_reqparse(module_role, newdata)
            module_role.save_to_db()
            return module_role.json()
        return {'message': 'No se encuentra Module_role'}, 404

    @jwt_required()
    @check('module_role_delete')
    @swag_from('../swagger/module_role/delete_module_role.yaml')
    def delete(self, id):
        module_role = ModuleRoleModel.find_by_id(id)
        if module_role:
            module_role.delete_from_db()

        return {'message': 'Se ha borrado Module_role'}


class ModuleRoleList(Resource):

    @jwt_required()
    @check('module_role_list')
    @swag_from('../swagger/module_role/list_module_role.yaml')
    def get(self):
        query = ModuleRoleModel.query
        return paginated_results(query)

    @jwt_required()
    @check('module_role_insert')
    @swag_from('../swagger/module_role/post_module_role.yaml')
    def post(self):
        data = ModuleRole.parser.parse_args()

        id = data.get('id')

        if id is not None and ModuleRoleModel.find_by_id(id):
            return {'message': "Ya existe un module_role con id '{}'.".format(id)}, 400

        module_role = ModuleRoleModel(**data)
        try:
            module_role.save_to_db()
        except Exception as e:
            logging.error('Ocurrió un error al crear Cliente.', exc_info=e)
            return {"message": "Ocurrió un error al crear Module_role."}, 500

        return module_role.json(), 201


class ModuleRoleSearch(Resource):

    @jwt_required()
    @check('module_role_search')
    @swag_from('../swagger/module_role/search_module_role.yaml')
    def post(self):
        query = ModuleRoleModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: ModuleRoleModel.id == x)
            query = restrict(query, filters, 'module_id', lambda x: ModuleRoleModel.module_id == x)
            query = restrict(query, filters, 'role_id', lambda x: ModuleRoleModel.role_id == x)

        # default order
        query = query.order_by(ModuleRoleModel.id.desc())
        return paginated_results(query)
