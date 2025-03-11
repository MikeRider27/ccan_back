import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _
from sqlalchemy.orm import aliased

from models.role import RoleModel
from models.user import UserModel
from models.user_role import UserRoleModel
from security import check
from utils import restrict, paginated_results, sha1_pass


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('user', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('firstname', type=str)
    parser.add_argument('lastname', type=str)
    parser.add_argument('administrator', type=bool)
    parser.add_argument('email', type=str)
    parser.add_argument('role_list', type=list, location='json', default=[])
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('user_get')
    @swag_from('../swagger/user/get_user.yaml')
    def get(self, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json()
        return {'message': _("USER_NOT_FOUND")}, 404

    @jwt_required()
    @check('user_update')
    @swag_from('../swagger/user/put_user.yaml')
    def put(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': _("USER_NOT_FOUND")}, 404

        newdata = User.parser.parse_args()
        UserModel.from_reqparse(user, newdata)

        # Hospital - Role administration
        old_ids = [hospital_role.id for hospital_role in user.role_list]
        new_ids = [hospital_role['id'] for hospital_role in newdata['role_list'] if 'id' in hospital_role]

        # Delete
        set_dif = set(old_ids).symmetric_difference(set(new_ids))
        to_delete = list(set_dif)
        for hospital_role_id in to_delete:
            hospital_role_to_delete = next(hospital_role for hospital_role in user.role_list if hospital_role.id == hospital_role_id)
            hospital_role_to_delete.delete_from_db()

        # Add
        to_add = [hospital_role for hospital_role in newdata['role_list'] if 'id' not in hospital_role]
        for hospital_role in to_add:
            if hospital_role:
                role = RoleModel.query.filter_by(description=hospital_role['role_description']).first()
                hospital_role_model = UserRoleModel(id=None, user_id=None,
                                                        role_id=role.id, hospital_id=hospital_role['hospital_id'])
                user.role_list.append(hospital_role_model)

        # Modify
        for hospital_role_id in new_ids:
            hospital_role_old = next(hospital_role for hospital_role in user.role_list if hospital_role.id == hospital_role_id)
            hospital_role_mod = next(hospital_role for hospital_role in newdata['role_list'] if hospital_role['id'] == hospital_role_id)
            if hospital_role_old.role.description != hospital_role_mod['role_description']:
                role = RoleModel.query.filter_by(description=hospital_role_mod['role_description']).first()
                hospital_role_old.role = role

        user.user_modify = get_jwt_identity()
        user.date_modify = datetime.now()
        user.save_to_db()
        return {'message': _("USER_UPDATE_SUCESSFULL")}, 200

    @jwt_required()
    @check('user_delete')
    @swag_from('../swagger/user/delete_user.yaml')
    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()

        return {'message': _("USER_DELETED")}


class UserList(Resource):

    @jwt_required()
    @check('user_list')
    @swag_from('../swagger/user/list_user.yaml')
    def get(self):
        query = UserModel.query
        return paginated_results(query)

    @jwt_required()
    @check('user_insert')
    @swag_from('../swagger/user/post_user.yaml')
    def post(self):
        data = User.parser.parse_args()

        id = data.get('id')
        if id is not None and UserModel.find_by_id(id):
            return {'message': _("USER_DUPLICATED").format(id)}, 400

        userName = data.get('user')
        if userName is not None and UserModel.query.filter_by(user=userName).first():
            return {'message': _("USER_DUPLICATED_NAME")}, 400

        if 'role_list' in data and data['role_list']:
            role_list = []
            for hospital_role in data['role_list']:
                if hospital_role:
                    role = RoleModel.query.filter_by(description=hospital_role['role_description']).first()
                    hospital_role_model = UserRoleModel(id=None, user_id=None,
                                                            role_id=role.id, hospital_id=hospital_role['hospital_id'])
                    role_list.append(hospital_role_model)
            del data['role_list']
            data.role_list = role_list

        user: UserModel = UserModel(**data)

        # Trim in username
        user.user = user.user.strip()
        try:
            user.user_create = get_jwt_identity()
            user.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating user', exc_info=e)
            return {"message": _("USER_CREATE_ERROR")}, 500

        return {'message': _("USER_CREATE_SUCESSFULL")}, 201


class UserSearch(Resource):

    @jwt_required()
    @check('user_search')
    @swag_from('../swagger/user/search_user.yaml')
    def post(self):
        query = UserModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: UserModel.id == x)
            query = restrict(query, filters, 'user', lambda x: UserModel.user.contains(x))
            query = restrict(query, filters, 'state', lambda x: UserModel.state.contains(x))
            query = restrict(query, filters, 'password', lambda x: UserModel.password.contains(x))
            query = restrict(query, filters, 'firstname', lambda x: UserModel.firstname.contains(x))
            query = restrict(query, filters, 'lastname', lambda x: UserModel.lastname.contains(x))
            query = restrict(query, filters, 'administrator', lambda x: x)
            query = restrict(query, filters, 'email', lambda x: UserModel.email.contains(x))
            query = restrict(query, filters, 'date_create', lambda x: func.to_char(UserModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: UserModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify', lambda x: func.to_char(UserModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: UserModel.user_modify.contains(x))

            if 'hospital_id_list' in filters and filters.get('hospital_id_list'):
                user_hospital = aliased(UserRoleModel)
                query = query.join(user_hospital)
                query = restrict(query, filters, 'hospital_id_list', lambda x: user_hospital.hospital_id.in_(x))

        return paginated_results(query)


class UserChangePass(Resource):
    @jwt_required()
    @check('user_change_password')
    @swag_from('../swagger/user/user_change_password.yaml')
    def put(self, username):
        user = UserModel.query.filter_by(user=username).first()
        if not user:
            return {'message': f"Usuario '{username}' no encontrado"}, 404

        data = request.json

        # Check user admin
        auth_username = get_jwt_identity()
        auth_user = UserModel.query.filter_by(user=auth_username).first()
        if auth_user:
            if not auth_user.administrator:
                if data['last_password']:   # Si el campo viene vacío, es un administrador por ROL y no el campo administrador
                    last_pass_encoded = sha1_pass(data['last_password'])
                    if user.password != last_pass_encoded:
                        return {'message': _("PASSWORD_CHANGE_ERROR")}, 400
        else:
            return {'message': _("USER_AUTH_NOT_FOUND")}, 404

        user.password = sha1_pass(data['new_password'])
        user.save_to_db()

        return {'message': _("PASSWORD_CHANGE_SUCESSFULL")}, 200
