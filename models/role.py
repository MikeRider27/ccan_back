import datetime

from db import db, BaseModel
from models.permission import PermissionModel


class RoleModel(BaseModel):
    __tablename__ = 'role'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    permissions = db.relationship(PermissionModel, secondary='role_permission')
    module_list = db.relationship('ModuleRoleModel')

    def __init__(self, id, description, permissions, date_create=None, module_list=None,
                 user_create=None, date_modify=None, user_modify=None):
        self.id = id
        self.description = description
        self.permissions = permissions
        self.module_list = module_list
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
        }

        if jsondepth > 0:
            json['permissions'] = [x.json() for x in self.permissions] if self.permissions else []

        if self.module_list:
            json['module_list'] = [x.json(jsondepth) for x in self.module_list]
        else:
            json['module_list'] = [{}]
        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

