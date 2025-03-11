import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.user_role import UserRoleModel
from utils import restrict, paginated_results
from security import check


class UserRole(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('user_id', type=int)
    parser.add_argument('role_id', type=int)
    parser.add_argument('hospital_id', type=int)


    @jwt_required()
    @check('user_role_get')
    @swag_from('../swagger/user_hospital/get_user_hospital.yaml')
    def get(self, id):
        user_hospital = UserRoleModel.find_by_id(id)
        if user_hospital:
            return user_hospital.json()
        return {'message': _("USER_HOSPITAL_NOT_FOUND")}, 404

    @jwt_required()
    @check('user_role_update')
    @swag_from('../swagger/user_hospital/put_user_hospital.yaml')
    def put(self, id):
        user_hospital = UserRoleModel.find_by_id(id)
        if user_hospital:
            newdata = UserRole.parser.parse_args()
            UserRoleModel.from_reqparse(user_hospital, newdata)
            user_hospital.save_to_db()
            return user_hospital.json()
        return {'message': _("USER_HOSPITAL_NOT_FOUND")}, 404

    @jwt_required()
    @check('user_role_delete')
    @swag_from('../swagger/user_hospital/delete_user_hospital.yaml')
    def delete(self, id):
        user_hospital = UserRoleModel.find_by_id(id)
        if user_hospital:
            user_hospital.delete_from_db()

        return {'message': _("USER_HOSPITAL_DELETED")}


class UserRoleList(Resource):

    @jwt_required()
    @check('user_role_list')
    @swag_from('../swagger/user_hospital/list_user_hospital.yaml')
    def get(self):
        hospital_id = request.args.get('hospital_id', None, int)
        role_id = request.args.get('role_id', None, int)
        query = UserRoleModel.query

        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)
        if role_id:
            query = query.filter_by(role_id=role_id)

        return paginated_results(query)

    @jwt_required()
    @check('user_role_insert')
    @swag_from('../swagger/user_hospital/post_user_hospital.yaml')
    def post(self):
        data = UserRole.parser.parse_args()

        id = data.get('id')

        if id is not None and UserRoleModel.find_by_id(id):
            return {'message': _("USER_HOSPITAL_DUPLICATED").format(id)}, 400

        user_hospital = UserRoleModel(**data)
        try:
            user_hospital.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating user hospital.', exc_info=e)
            return {"message": _("USER_HOSPITAL_CREATE_ERROR")}, 500

        return user_hospital.json(), 201


class UserRoleSearch(Resource):

    @jwt_required()
    @check('user_role_search')
    @swag_from('../swagger/user_hospital/search_user_hospital.yaml')
    def post(self):
        query = UserRoleModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: UserRoleModel.id == x)
            query = restrict(query, filters, 'user_id', lambda x: UserRoleModel.user_id == x)
            query = restrict(query, filters, 'role_id', lambda x: UserRoleModel.role_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: UserRoleModel.hospital_id == x)
        return paginated_results(query)
