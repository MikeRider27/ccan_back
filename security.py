from flask_jwt_extended import get_jwt_identity, get_jwt
from functools import wraps
from flask_babel import _
from models.hospital import HospitalModel
from models.module import ModuleModel
from models.module_permission import ModulePermissionModel
from models.module_role import ModuleRoleModel
from models.permission import PermissionModel
from models.role import RoleModel
from models.role_permission import RolePermissionModel

from models.user import UserModel
from models.user_role import UserRoleModel


def flat_map(f, xs):
    return [y for ys in xs for y in f(ys)]
#
# def check2(permission):
#     def wrfunc(fn):
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             user = get_jwt_identity()
#             if user is None:
#                 return {'message': _('NO_PERMISSION')}, 401
#             model = UserModel.query.filter_by(user=user).first()
#             claims = get_jwt()
#             if model.administrator:
#               return fn(*args, **kwargs)
#             # if permission in flat_map(lambda x: x['permission'], claims['permissions']):
#             #   return fn(*args, **kwargs)
#             uhm = UserRoleModel.query\
#                 .join(HospitalModel)\
#                 .join(UserModel)\
#                 .filter(
#                     UserModel.user == user,
#                     HospitalModel.id.in_(map(lambda x: x['hospital_id'], claims['roles']))
#                 ).all()
#             if not uhm or len(uhm) == 0:
#                 return {'message': _('NO_PERMISSION')}, 401
#             per = list(map(lambda x: x.description, list(flat_map(lambda x: x.role.permissions, uhm))))
#             if permission not in per:
#                 return {'message': _('NO_PERMISSION')}, 401
#             # for element in claims['permisions']:
#             #     if permission not in element['permiso']:
#             #         return {'message': 'No tiene permisos para realizar esta acción'}, 401
#             return fn(*args, **kwargs)
#         return wrapper
#     return wrfunc

def check(permission):
    def wrfunc(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()
            if user is None:
                return {'message': _('NO_PERMISSION')}, 401

            user_model = UserModel.query.filter_by(user=user).first()
            if user_model is None:
                return {'message': _('NO_PERMISSION')}, 401

            if user_model.administrator:
                return fn(*args, **kwargs)

            query_rol = (PermissionModel.query
                     .join(RolePermissionModel, RolePermissionModel.permission_id == PermissionModel.id)
                     .join(UserRoleModel, UserRoleModel.role_id == RolePermissionModel.role_id)
                     .filter(UserRoleModel.user_id == user_model.id, PermissionModel.description == permission))

            query_modulo = (PermissionModel.query
                      .join(ModulePermissionModel, ModulePermissionModel.permission_id == PermissionModel.id)
                      .join(ModuleModel, ModuleModel.id == ModulePermissionModel.module_id)
                      .join(ModuleRoleModel, ModuleRoleModel.module_id == ModuleModel.id)
                      .join(UserRoleModel, UserRoleModel.role_id == ModuleRoleModel.role_id)
                     .filter(UserRoleModel.user_id == user_model.id, PermissionModel.description == permission))

            #permission_list = query.all()
            permission_list = query_rol.all() + query_modulo.all()

            if not permission_list:
                return {'message': _('NO_PERMISSION')}, 401

            return fn(*args, **kwargs)
        return wrapper
    return wrfunc


def check_hospital(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        identity = get_jwt()
        hospital_id = identity.get('hospital_id', 0)
        if not hospital_id:
            return {'message': _('USER_HOSPITAL_NOT_FOUND')}, 403

        return f(hospital_id=hospital_id, *args, **kwargs)

    return decorator

