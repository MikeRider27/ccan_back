import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.hospital import HospitalModel
from models.parameter import ParameterModel
from models.patient import OriginsCode


class DepositModel(BaseModel):
    __tablename__ = 'deposit'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    type_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    city = db.Column(db.String(20))
    address = db.Column(db.String(100))
    email = db.Column(db.String(20))
    phone = db.Column(db.String(30))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)
    origin = db.Column(db.String(30), nullable=False, default=OriginsCode.CCAN_CITY_SOFT.value)

    # Relationship
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)
    type = db.relationship('ParameterModel', foreign_keys=[type_id], uselist=False)

    def __init__(self, id=None, code=None, type_id=None, name=None, description=None, city=None, address=None,
                 email=None, phone=None, date_create=None, user_create=None, date_modify=None, user_modify=None,
                 hospital_id=None, origin=None):
        self.id = id
        self.code = code
        self.type_id = type_id
        self.name = name
        self.description = description
        self.city = city
        self.address = address
        self.email = email
        self.phone = phone
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.hospital_id = hospital_id
        self.origin = origin

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'city': self.city,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'hospital_id': self.hospital_id,
            'type_id': self.type_id,
            'origin': self.origin
        }

        if jsondepth > 0:
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
            if self.type:
                json['type'] = self.type.json(jsondepth - 1)

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

