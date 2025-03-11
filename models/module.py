import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.permission import PermissionModel


class ModuleModel(BaseModel):
    __tablename__ = 'module'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    permissions = db.relationship(PermissionModel, secondary='module_permission')


    def __init__(self, id=None, description=None, date_create=None, user_create=None, date_modify=None, permissions=None,
                 user_modify=None):
        self.id = id
        self.description = description
        self.permissions = permissions
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'date_create': self.date_create,
            'user_create': self.user_create,
            'date_modify': self.date_modify,
            'user_modify': self.user_modify,
        }

        if jsondepth > 0:
            json['permissions'] = [x.json() for x in self.permissions] if self.permissions else []

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
