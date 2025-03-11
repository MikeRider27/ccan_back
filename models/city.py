import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.area import AreaModel



class CityModel(BaseModel):
    __tablename__ = 'city'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String)
    area_id = db.Column(db.BigInteger, db.ForeignKey(AreaModel.id), nullable=False)

    area = db.relationship('AreaModel', foreign_keys=[area_id], uselist=False)

    def __init__(self, id, description, area_id):
        self.id = id
        self.description = description
        self.area_id = area_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'area_id': self.area_id
        }

        if jsondepth > 0:
            if self.area:
                json['area'] = self.area.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

