import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class MedicalDocumentTypeModel(BaseModel):
    __tablename__ = 'medical_document_type'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    orden = db.Column(db.Integer)
    code = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    def __init__(self, id=None, description=None, orden=None, code=None, active=None):
        self.id = id
        self.description = description
        self.orden = orden
        self.code = code
        self.active = active

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'orden': self.orden,
            'code': self.code,
            'active': self.active
        }
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

