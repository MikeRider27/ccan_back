import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.deposit import DepositModel
from models.stock import StockModel


class DepositStockModel(BaseModel):
    __tablename__ = 'deposit_stock'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    deposit_id = db.Column(db.BigInteger, db.ForeignKey(DepositModel.id), nullable=False)
    stock_id = db.Column(db.BigInteger, db.ForeignKey(StockModel.id), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    deposit = db.relationship('DepositModel', foreign_keys=[deposit_id], uselist=False)
    stock = db.relationship('StockModel', foreign_keys=[stock_id], uselist=False)
    entries_deposit_stock_list = db.relationship('EntriesDepositStockModel', back_populates='deposit_stock')

    def __init__(self, id=None, deposit_id=None, stock_id=None, quantity=None):
        self.id = id
        self.deposit_id = deposit_id
        self.stock_id = stock_id
        self.quantity = quantity

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'deposit_id': self.deposit_id,
            'stock_id': self.stock_id,
            'quantity': self.quantity,
        }

        if jsondepth > 0:
            if self.deposit:
                json['deposit'] = self.deposit.json(jsondepth - 1)
            if self.stock:
                json['stock'] = self.stock.json(jsondepth - 1)
            json['entries_deposit_stock_list'] = []
            if self.entries_deposit_stock_list:
                for entries_deposit_stock in self.entries_deposit_stock_list:
                    json['entries_deposit_stock_list'].append(entries_deposit_stock.json(jsondepth - 1))
        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

