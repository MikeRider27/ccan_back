import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.patient import OriginsCode


class SpecialtyModel(BaseModel):
    __tablename__ = 'specialty'

    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(300))
    origin = db.Column(db.String, default=OriginsCode.CCAN_CITY_SOFT.value)

    def __init__(self, id=None, description=None, origin=None):
        self.id = id
        self.description = description
        self.origin = origin

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'origin': self.origin
        }

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
