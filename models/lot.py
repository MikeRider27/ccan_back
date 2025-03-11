import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.patient import OriginsCode


class LotModel(BaseModel):
    __tablename__ = 'lot'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    num_lot = db.Column(db.String(50), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    origin = db.Column(db.String(30), nullable=False, default=OriginsCode.CCAN_CITY_SOFT.value)
    date = db.Column(db.DateTime, nullable=False)

    entries_list = db.relationship('EntriesModel', secondary='inventory.entries_lot')

    def __init__(self, id=None, num_lot=None, date_create=None, user_create=None, date_modify=None, user_modify=None, origin=None, date=None):
        self.id = id
        self.num_lot = num_lot
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.origin = origin
        self.date = date

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'num_lot': self.num_lot,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'origin': self.origin,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
        }

        if jsondepth > 0:
            json['entries_list'] = []
            if self.entries_list:
                for lot_detail in self.entries_list:
                    json['entries_list'].append(lot_detail.json(jsondepth - 1))

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

