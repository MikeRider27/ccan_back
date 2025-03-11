import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class ConfigurationModel(BaseModel):
    __tablename__ = 'configuration'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.String(50))
    code = db.Column(db.String(50))


    def __init__(self, id=None, name=None, value=None, code=None):
        self.id = id
        self.name = name
        self.value = value
        self.code = code

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'code': self.code,
        }

        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

