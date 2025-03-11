import base64
import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.module import ModuleModel
from models.permission import PermissionModel
from utils import restrict, paginated_results
from security import check
from flask_babel import _


class Module(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('permissions',  type=list, location='json')
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('module_get')
    @swag_from('../swagger/module/get_module.yaml')
    def get(self, id):
        module = ModuleModel.find_by_id(id)
        if module:
            return module.json()
        return {'message': 'No se encuentra Module'}, 404

    @jwt_required()
    @check('module_update')
    @swag_from('../swagger/module/put_module.yaml')
    def put(self, id):
        module = ModuleModel.find_by_id(id)
        if module:
            newdata = Module.parser.parse_args()
            module.from_reqparse(module, newdata)

            # Get Permission from BD
            if 'permissions' in newdata and newdata['permissions'] is not None:
                permission_list = []
                for permission in newdata['permissions']:
                    permissionModel = PermissionModel.query.filter_by(description=permission).first()
                    if permissionModel:
                        permission_list.append(permissionModel)
                module.permissions = permission_list

            module.user_modify = get_jwt_identity()
            module.date_modify = datetime.now()
            module.save_to_db()
            return module.json()
        return {'message': _("MODULE_NOT_FOUND")}, 404

    @jwt_required()
    @check('module_delete')
    @swag_from('../swagger/module/delete_module.yaml')
    def delete(self, id):
        module = ModuleModel.find_by_id(id)
        if module:
            module.delete_from_db()

        return {'message': 'Se ha borrado Module'}


class ModuleList(Resource):

    @jwt_required()
    @check('module_list')
    @swag_from('../swagger/module/list_module.yaml')
    def get(self):
        query = ModuleModel.query
        return paginated_results(query)

    @jwt_required()
    @check('module_insert')
    @swag_from('../swagger/role/post_role.yaml')
    def post(self):
        data = Module.parser.parse_args()

        id = data.get('id')

        if id is not None and ModuleModel.find_by_id(id):
            return {'message': _("MODULE_DUPLICATED").format(id)}, 400

        # Get Permission from BD
        if 'permissions' in data and data['permissions'] is not None:
            permission_list = []
            for permission in data['permissions']:
                permissionModel = PermissionModel.query.filter_by(description=permission).first()
                if permissionModel:
                    permission_list.append(permissionModel)
            data.permissions = permission_list

        module = ModuleModel(**data)

        try:
            module.user_create = get_jwt_identity()
            module.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating module.', exc_info=e)
            return {"message": _("MODULE_CREATE_ERROR")}, 500

        return module.json(), 201


class ModuleSearch(Resource):

    @jwt_required()
    @check('module_search')
    @swag_from('../swagger/module/search_module.yaml')
    def post(self):
        query = ModuleModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: ModuleModel.id == x)
            query = restrict(query, filters, 'description', lambda x: ModuleModel.description.contains(x))
            query = restrict(query, filters, 'user_create', lambda x: ModuleModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: ModuleModel.user_modify.contains(x))

        # default order
        query = query.order_by(ModuleModel.id.desc())
        return paginated_results(query)
