import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.entries import EntriesModel
from models.deposit_stock import DepositStockModel


class EntriesDepositStockModel(BaseModel):
    __tablename__ = 'entries_deposit_stock'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    entries_id = db.Column(db.BigInteger, db.ForeignKey(EntriesModel.id))
    deposit_stock_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id))

    # Relationship
    entries = db.relationship('EntriesModel', foreign_keys=[entries_id], uselist=False)
    deposit_stock = db.relationship('DepositStockModel', foreign_keys=[deposit_stock_id], uselist=False)

    def __init__(self, id=None, entries_id=None, deposit_stock_id=None):
        self.id = id
        self.entries_id = entries_id
        self.deposit_stock_id = deposit_stock_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'entries_id': self.entries_id,
            'deposit_stock_id': self.deposit_stock_id,
        }

        if jsondepth > 0:
            if self.entries:
                json['entries'] = self.entries.json(jsondepth - 1)
            if self.deposit_stock:
                json['deposit_stock'] = self.deposit_stock.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

