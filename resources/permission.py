import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.permission import PermissionModel
from utils import restrict, paginated_results
from security import check


class Permission(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)

    @jwt_required()
    @check('permission_get')
    @swag_from('../swagger/permission/get_permission.yaml')
    def get(self, id):
        permission = PermissionModel.find_by_id(id)
        if permission:
            return permission.json()
        return {'message': _("PERMISSION_NOT_FOUND")}, 404

    @jwt_required()
    @check('permission_update')
    @swag_from('../swagger/permission/put_permission.yaml')
    def put(self, id):
        permission = PermissionModel.find_by_id(id)
        if permission:
            newdata = Permission.parser.parse_args()
            PermissionModel.from_reqparse(permission, newdata)
            permission.save_to_db()
            return permission.json()
        return {'message': _("PERMISSION_NOT_FOUND")}, 404

    @jwt_required()
    @check('permission_delete')
    @swag_from('../swagger/permission/delete_permission.yaml')
    def delete(self, id):
        permission = PermissionModel.find_by_id(id)
        if permission:
            permission.delete_from_db()

        return {'message': _("PERMISSION_DELETED")}


class PermissionList(Resource):

    @jwt_required()
    @check('permission_list')
    @swag_from('../swagger/permission/list_permission.yaml')
    def get(self):
        query = PermissionModel.query
        return paginated_results(query)

    @jwt_required()
    @check('permission_insert')
    @swag_from('../swagger/permission/post_permission.yaml')
    def post(self):
        data = Permission.parser.parse_args()

        id = data.get('id')
        if id is not None and PermissionModel.find_by_id(id):
            return {'message': _("PERMISSION_DUPLICATED").format(id)}, 400

        description = data.get('description')
        permission = PermissionModel.query.filter_by(description=description).first()
        if description is not None and permission:
            return {'message': _("PERMISSION_DUPLICATED").format(description)}, 400

        permission = PermissionModel(**data)
        try:
            permission.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating permission.', exc_info=e)
            return {"message": _("PERMISSION_CREATE_ERROR")}, 500

        return permission.json(), 201


class PermissionSearch(Resource):

    @jwt_required()
    @check('permission_search')
    @swag_from('../swagger/permission/search_permission.yaml')
    def post(self):
        query = PermissionModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PermissionModel.id == x)
            query = restrict(query, filters, 'description', lambda x: PermissionModel.description.contains(x))
        return paginated_results(query)
