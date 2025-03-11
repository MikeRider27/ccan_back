import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.role import RoleModel
from models.permission import PermissionModel


class RolePermissionModel(BaseModel):
    __tablename__ = 'role_permission'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey(RoleModel.id), nullable=False)
    permission_id = db.Column(db.BigInteger, db.ForeignKey(PermissionModel.id), nullable=False)

    role = db.relationship('RoleModel', foreign_keys=[role_id], uselist=False)
    permission = db.relationship('PermissionModel', foreign_keys=[permission_id], uselist=False)

    def __init__(self, id, role_id, permission_id):
        self.id = id
        self.role_id = role_id
        self.permission_id = permission_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
        }

        if jsondepth > 0:
            if self.role:
                json['role'] = self.role.json(jsondepth - 1)
            if self.permission:
                json['permission'] = self.permission.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

