import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class Cie_10Model(BaseModel):
    __tablename__ = 'cie_10'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description_es = db.Column(db.String(500), nullable=False)
    description_en = db.Column(db.String(500))


    def __init__(self, id, code, description_es, description_en):
        self.id = id
        self.code = code
        self.description_es = description_es
        self.description_en = description_en

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'code': self.code,
            'description_es': self.description_es,
            'description_en': self.description_en,
        }

        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

