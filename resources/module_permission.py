import base64
import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.module_permission import ModulePermissionModel
from utils import restrict, paginated_results
from security import check


class ModulePermission(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('module_id', type=int)
    parser.add_argument('permission_id', type=int)

    @jwt_required()
    @check('module_permission_get')
    @swag_from('../swagger/module_permission/get_module_permission.yaml')
    def get(self, id):
        module_permission = ModulePermissionModel.find_by_id(id)
        if module_permission:
            return module_permission.json()
        return {'message': 'No se encuentra Module_permission'}, 404

    @jwt_required()
    @check('module_permission_update')
    @swag_from('../swagger/module_permission/put_module_permission.yaml')
    def put(self, id):
        module_permission = ModulePermissionModel.find_by_id(id)
        if module_permission:
            newdata = ModulePermission.parser.parse_args()
            ModulePermissionModel.from_reqparse(module_permission, newdata)
            module_permission.save_to_db()
            return module_permission.json()
        return {'message': 'No se encuentra Module_permission'}, 404

    @jwt_required()
    @check('module_permission_delete')
    @swag_from('../swagger/module_permission/delete_module_permission.yaml')
    def delete(self, id):
        module_permission = ModulePermissionModel.find_by_id(id)
        if module_permission:
            module_permission.delete_from_db()

        return {'message': 'Se ha borrado Module_permission'}


class ModulePermissionList(Resource):

    @jwt_required()
    @check('module_permission_list')
    @swag_from('../swagger/module_permission/list_module_permission.yaml')
    def get(self):
        query = ModulePermissionModel.query
        return paginated_results(query)

    @jwt_required()
    @check('module_permission_insert')
    @swag_from('../swagger/module_permission/post_module_permission.yaml')
    def post(self):
        data = ModulePermission.parser.parse_args()

        id = data.get('id')

        if id is not None and ModulePermissionModel.find_by_id(id):
            return {'message': "Ya existe un module_permission con id '{}'.".format(id)}, 400

        module_permission = ModulePermissionModel(**data)
        try:
            module_permission.save_to_db()
        except Exception as e:
            logging.error('Ocurrió un error al crear Cliente.', exc_info=e)
            return {"message": "Ocurrió un error al crear Module_permission."}, 500

        return module_permission.json(), 201


class ModulePermissionSearch(Resource):

    @jwt_required()
    @check('module_permission_search')
    @swag_from('../swagger/module_permission/search_module_permission.yaml')
    def post(self):
        query = ModulePermissionModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: ModulePermissionModel.id == x)
            query = restrict(query, filters, 'module_id', lambda x: ModulePermissionModel.module_id == x)
            query = restrict(query, filters, 'permission_id', lambda x: ModulePermissionModel.permission_id == x)

        # default order
        query = query.order_by(ModulePermissionModel.id.desc())
        return paginated_results(query)
