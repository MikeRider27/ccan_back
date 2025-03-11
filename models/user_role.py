import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.user import UserModel
from models.role import RoleModel
from models.hospital import HospitalModel

class UserRoleModel(BaseModel):
    __tablename__ = 'user_role'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(UserModel.id), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey(RoleModel.id), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)

    user = db.relationship('UserModel', foreign_keys=[user_id], uselist=False)
    role = db.relationship('RoleModel', foreign_keys=[role_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def __init__(self, id, user_id, role_id, hospital_id):
        self.id = id
        self.user_id = user_id
        self.role_id = role_id
        self.hospital_id = hospital_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'hospital_id': self.hospital_id
        }

        if jsondepth > 0:
            if self.user:
                json['user'] = self.user.json(jsondepth - 1)
            if self.role:
                json['role'] = self.role.json(jsondepth - 1)
                json['role_description'] = json['role']['description']
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

