import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.country import CountryModel
from models.parameter import ParameterModel


class ManufacturerModel(BaseModel):
    __tablename__ = 'manufacturer'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    county_id = db.Column(db.BigInteger, db.ForeignKey(CountryModel.id))
    state_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    parameter = db.relationship('ParameterModel', foreign_keys=[state_id], uselist=False)
    country = db.relationship('CountryModel', foreign_keys=[county_id], uselist=False)

    def __init__(self, id, name, county_id, state_id, date_create, user_create, date_modify, user_modify):
        self.id = id
        self.name = name
        self.county_id = county_id
        self.state_id = state_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'name': self.name,
            'county_id': self.county_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'state_id': self.state_id
        }

        if jsondepth > 0:
            if self.parameter:
                json['parameter'] = self.parameter.json(jsondepth - 1)
            if self.country:
                json['country'] = self.country.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

