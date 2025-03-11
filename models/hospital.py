import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.country import CountryModel


class HospitalModel(BaseModel):
    __tablename__ = 'hospital'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.BigInteger, db.ForeignKey(CountryModel.id), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    system = db.Column(db.Boolean, default=True)
    hospital_codigo = db.Column(db.String(100))

    # Relationship
    country = db.relationship('CountryModel', foreign_keys=[country_id], uselist=False)

    def __init__(self, id=None, description=None, country_id=None, date_create=None, user_create=None, date_modify=None,
                 user_modify=None, system=None, hospital_codigo=None):
        self.id = id
        self.description = description
        self.country_id = country_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.system = system
        self.hospital_codigo = hospital_codigo

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'system': self.system,
            'hospital_codigo': self.hospital_codigo,
        }

        if jsondepth > 0:
            if self.country:
                json['country'] = self.country.json(jsondepth - 1)

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

