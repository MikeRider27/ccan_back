import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.country import CountryModel



class AreaModel(BaseModel):
    __tablename__ = 'area'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String)
    country_id = db.Column(db.BigInteger, db.ForeignKey(CountryModel.id), nullable=False)
    area_number = db.Column(db.Integer)

    country = db.relationship('CountryModel', foreign_keys=[country_id], uselist=False)

    def __init__(self, id, description, country_id, area_number):
        self.id = id
        self.description = description
        self.country_id = country_id
        self.area_number = area_number

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'country_id': self.country_id,
            'area_number': self.area_number
        }

        if jsondepth > 0:
            if self.country:
                json['country'] = self.country.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

