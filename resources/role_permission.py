import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.role_permission import RolePermissionModel
from utils import restrict, paginated_results
from security import check


class RolePermission(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('role_id', type=int)
    parser.add_argument('permission_id', type=int)

    @jwt_required()
    @check('role_permission_get')
    @swag_from('../swagger/role_permission/get_role_permission.yaml')
    def get(self, id):
        role_permission = RolePermissionModel.find_by_id(id)
        if role_permission:
            return role_permission.json()
        return {'message': _("ROL_PERMISSION_NOT_FOUND")}, 404

    @jwt_required()
    @check('role_permission_update')
    @swag_from('../swagger/role_permission/put_role_permission.yaml')
    def put(self, id):
        role_permission = RolePermissionModel.find_by_id(id)
        if role_permission:
            newdata = RolePermission.parser.parse_args()
            RolePermissionModel.from_reqparse(role_permission, newdata)
            role_permission.save_to_db()
            return role_permission.json()
        return {'message': _("ROL_PERMISSION_NOT_FOUND")}, 404

    @jwt_required()
    @check('role_permission_delete')
    @swag_from('../swagger/role_permission/delete_role_permission.yaml')
    def delete(self, id):
        role_permission = RolePermissionModel.find_by_id(id)
        if role_permission:
            role_permission.delete_from_db()

        return {'message': _("ROL_PERMISSION_DELETED")}


class RolePermissionList(Resource):

    @jwt_required()
    @check('role_permission_list')
    @swag_from('../swagger/role_permission/list_role_permission.yaml')
    def get(self):
        query = RolePermissionModel.query
        return paginated_results(query)

    @jwt_required()
    @check('role_permission_insert')
    @swag_from('../swagger/role_permission/post_role_permission.yaml')
    def post(self):
        data = RolePermission.parser.parse_args()

        id = data.get('id')

        if id is not None and RolePermissionModel.find_by_id(id):
            return {'message': _("ROL_PERMISSION_DUPLICATED").format(id)}, 400

        role_permission = RolePermissionModel(**data)
        try:
            role_permission.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating rol permission.', exc_info=e)
            return {"message": _("ROL_PERMISSION_CREATE_ERROR")}, 500

        return role_permission.json(), 201


class RolePermissionSearch(Resource):

    @jwt_required()
    @check('role_permission_search')
    @swag_from('../swagger/role_permission/search_role_permission.yaml')
    def post(self):
        query = RolePermissionModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: RolePermissionModel.id == x)
            query = restrict(query, filters, 'role_id', lambda x: RolePermissionModel.role_id == x)
            query = restrict(query, filters, 'permission_id', lambda x: RolePermissionModel.permission_id == x)
        return paginated_results(query)
