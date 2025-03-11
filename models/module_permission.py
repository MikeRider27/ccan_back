import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.module import ModuleModel
from models.permission import PermissionModel


class ModulePermissionModel(BaseModel):
    __tablename__ = 'module_permission'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.BigInteger, db.ForeignKey(ModuleModel.id))
    permission_id = db.Column(db.BigInteger, db.ForeignKey(PermissionModel.id))

    module = db.relationship('ModuleModel', foreign_keys=[module_id], uselist=False)
    permission = db.relationship('PermissionModel', foreign_keys=[permission_id], uselist=False)

    def __init__(self, id=None, module_id=None, permission_id=None):
        self.id = id
        self.module_id = module_id
        self.permission_id = permission_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
        }

        if jsondepth > 0:
            if self.module:
                json['module'] = self.module.json(jsondepth - 1)
            if self.permission:
                json['permission'] = self.permission.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
