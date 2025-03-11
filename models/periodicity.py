import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class PeriodicityModel(BaseModel):
    __tablename__ = 'periodicity'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean)
    code = db.Column(db.String(20))

    def __init__(self, id=None, description=None, active=None, code=None):
        self.id = id
        self.description = description
        self.active = active
        self.code = code

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'active': self.active,
            'code': self.code
        }

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
