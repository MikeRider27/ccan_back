import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.patient import OriginsCode


class DoctorModel(BaseModel):
    __tablename__ = 'doctor'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    registry_number = db.Column(db.String(50))
    document_number = db.Column(db.String(50), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    origin = db.Column(db.String, default=OriginsCode.CCAN_CITY_SOFT.value)

    # Relationship
    specialty_list = db.relationship('DoctorSpecialtyModel', cascade="all, delete-orphan")

    def __init__(self, id=None, firstname=None, lastname=None, registry_number=None, document_number=None,
                 date_create=None, user_create=None, date_modify=None, user_modify=None, origin=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.registry_number = registry_number
        self.document_number = document_number
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.origin = origin

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'registry_number': self.registry_number,
            'document_number': self.document_number,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'origin': self.origin,
        }

        if jsondepth > 0:
            json['specialty_list'] = []
            if self.specialty_list:
                for specialty in self.specialty_list:
                    json['specialty_list'].append(specialty.json(jsondepth - 1))

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
