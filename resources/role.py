import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.module_role import ModuleRoleModel
from models.permission import PermissionModel
from models.role import RoleModel
from security import check
from utils import restrict, paginated_results
from security import check


class Role(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('permissions',  type=list, location='json')
    parser.add_argument('module_list', type=list, location='json', default=[])
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('role_get')
    @swag_from('../swagger/role/get_role.yaml')
    def get(self, id):
        role = RoleModel.find_by_id(id)
        if role:
            return role.json()
        return {'message': _("ROL_NOT_FOUND")}, 404

    @jwt_required()
    @check('role_update')
    @swag_from('../swagger/role/put_role.yaml')
    def put(self, id):
        role = RoleModel.find_by_id(id)
        if role:
            newdata = Role.parser.parse_args()
            role.from_reqparse(role, newdata)

            # Get Permission from BD
            if 'permissions' in newdata and newdata['permissions'] is not None:
                permission_list = []
                for permission in newdata['permissions']:
                    permissionModel = PermissionModel.query.filter_by(description=permission).first()
                    if permissionModel:
                        permission_list.append(permissionModel)
                role.permissions = permission_list

            if 'module_list' in newdata and newdata['module_list'] is not None:

                role_old_ids = list(map(lambda x: x.id, role.module_list))
                role_new_ids = list(filter(lambda x: x is not None, map(lambda x: x.get('id'), newdata['module_list'])))
                to_delete = list(set(role_old_ids) - set(role_new_ids))
                to_add = list(filter(lambda x: x.get('id') is None, newdata['module_list']))


                for role_module_id in to_delete:
                    role_module_to_delete = next(role_module for role_module in role.module_list if
                                                   role_module.id == role_module_id)
                    role_module_to_delete.delete_from_db()

                # Add
                #to_add = [role_module for role_module in newdata['module_list'] if 'id' not in role_module]
                for role_module in to_add:
                    if role_module:
                        role_module_model = ModuleRoleModel(id=None, module_id=role_module['module_id'])
                        role.module_list.append(role_module_model)



            role.user_modify = get_jwt_identity()
            role.date_modify = datetime.now()
            role.save_to_db()
            return role.json()
        return {'message': _("ROL_NOT_FOUND")}, 404

    @jwt_required()
    @check('role_delete')
    @swag_from('../swagger/role/delete_role.yaml')
    def delete(self, id):
        role = RoleModel.find_by_id(id)
        if role:
            role.delete_from_db()

        return {'message': _("ROL_DELETED")}


class RoleList(Resource):

    @jwt_required()
    @check('role_list')
    @swag_from('../swagger/role/list_role.yaml')
    def get(self):
        query = RoleModel.query
        return paginated_results(query)

    @jwt_required()
    @check('role_insert')
    @swag_from('../swagger/role/post_role.yaml')
    def post(self):
        data = Role.parser.parse_args()

        id = data.get('id')

        if id is not None and RoleModel.find_by_id(id):
            return {'message': _("ROL_DUPLICATED").format(id)}, 400

        # Get Permission from BD
        if 'permissions' in data and data['permissions'] is not None:
            permission_list = []
            for permission in data['permissions']:
                permissionModel = PermissionModel.query.filter_by(description=permission).first()
                if permissionModel:
                    permission_list.append(permissionModel)
            data.permissions = permission_list

        if 'module_list' in data and data['module_list']:
            module_list = []
            for role_module in data['module_list']:
                if role_module:
                    role_module_model = ModuleRoleModel(id=None, module_id=role_module['module_id'])
                    module_list.append(role_module_model)
            del data['module_list']
            data.module_list = module_list

        role = RoleModel(**data)

        try:
            role.user_create = get_jwt_identity()
            role.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating rol.', exc_info=e)
            return {"message": _("ROL_CREATE_ERROR")}, 500

        return role.json(), 201


class RoleSearch(Resource):

    @jwt_required()
    @check('role_search')
    @swag_from('../swagger/role/search_role.yaml')
    def post(self):
        query = RoleModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: RoleModel.id == x)
            query = restrict(query, filters, 'description', lambda x: RoleModel.description.contains(x))
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(RoleModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: RoleModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(RoleModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: RoleModel.user_modify.contains(x))
        return paginated_results(query)
