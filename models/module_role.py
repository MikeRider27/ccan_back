import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.module import ModuleModel
from models.role import RoleModel


class ModuleRoleModel(BaseModel):
    __tablename__ = 'module_role'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.BigInteger, db.ForeignKey(ModuleModel.id))
    role_id = db.Column(db.BigInteger, db.ForeignKey(RoleModel.id))

    module = db.relationship('ModuleModel', foreign_keys=[module_id], uselist=False)
    role = db.relationship('RoleModel', foreign_keys=[role_id], uselist=False)

    def __init__(self, id=None, module_id=None, role_id=None):
        self.id = id
        self.module_id = module_id
        self.role_id = role_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'module_id': self.module_id,
            'role_id': self.role_id,
        }

        if jsondepth > 0:
            if self.module:
                json['module'] = self.module.json(jsondepth - 1)
            if self.role:
                json['role'] = self.role.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
