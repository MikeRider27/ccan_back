import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class CieOMorphologyModel(BaseModel):
    __tablename__ = 'cie_o_morphology'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    term_en = db.Column(db.String)
    term_es = db.Column(db.String)
    code = db.Column(db.String)

    def __init__(self, id, term_en, term_es, code):
        self.id = id
        self.term_en = term_en
        self.term_es = term_es
        self.code = code
    
    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'term_en': self.term_en,
            'term_es': self.term_es,
            'code': self.code
        }
        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

