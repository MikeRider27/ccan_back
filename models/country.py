import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class CountryModel(BaseModel):
    __tablename__ = 'country'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)

    def __init__(self, id, description, code, nationality):
        self.id = id
        self.description = description
        self.code = code
        self.nationality = nationality

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'code': self.code,
            'nationality': self.nationality,
        }

        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

