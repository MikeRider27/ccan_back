import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.lot import LotModel
from models.entries import EntriesModel


class EntriesLotModel(BaseModel):
    __tablename__ = 'entries_lot'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    lot_id = db.Column(db.BigInteger, db.ForeignKey(LotModel.id))
    entries_id = db.Column(db.BigInteger, db.ForeignKey(EntriesModel.id))

    lot = db.relationship('LotModel', foreign_keys=[lot_id], uselist=False)
    entries = db.relationship('EntriesModel', foreign_keys=[entries_id], uselist=False)

    def __init__(self, id=None, lot_id=None, entries_id=None):
        self.id = id
        self.lot_id = lot_id
        self.entries_id = entries_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
        }

        if jsondepth > 0:
            if self.lot:
                json['lot'] = self.lot.json(jsondepth - 1)
            if self.entries:
                json['entries'] = self.entries.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

