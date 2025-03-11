import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class PermissionModel(BaseModel):
    __tablename__ = 'permission'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)


    def __init__(self, id, description):
        self.id = id
        self.description = description

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
        }

        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

