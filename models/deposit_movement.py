import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.deposit_stock import DepositStockModel
from models.lot import LotModel


class DepositMovementModel(BaseModel):
    __tablename__ = 'deposit_movement'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    deposit_stock_in_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id), nullable=False)
    deposit_stock_out_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    date_create = db.Column(db.DateTime, nullable=False)
    user_create = db.Column(db.String(30), nullable=False)
    lote_id = db.Column(db.BigInteger, db.ForeignKey(LotModel.id))

    deposit_stock_in = db.relationship('DepositStockModel', foreign_keys=[deposit_stock_in_id], uselist=False)
    deposit_stock_out = db.relationship('DepositStockModel', foreign_keys=[deposit_stock_out_id], uselist=False)
    lote = db.relationship('LotModel', foreign_keys=[lote_id], uselist=False)

    def __init__(self, id=None, deposit_stock_in_id=None, deposit_stock_out_id=None, quantity=None, date_create=None, user_create=None, lote_id=None):
        self.id = id
        self.deposit_stock_in_id = deposit_stock_in_id
        self.deposit_stock_out_id = deposit_stock_out_id
        self.quantity = quantity
        self.date_create = date_create
        self.user_create = user_create
        self.lote_id = lote_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'deposit_stock_in_id': self.deposit_stock_in_id,
            'deposit_stock_out_id': self.deposit_stock_out_id,
            'quantity': self.quantity,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M") if self.date_create else None,
            'user_create': self.user_create,
            'lote_id': self.lote_id,
        }

        if jsondepth > 0:
            if self.deposit_stock_in:
                json['deposit_stock_in'] = self.deposit_stock_in.json(jsondepth - 1)
            if self.deposit_stock_out:
                json['deposit_stock_out'] = self.deposit_stock_out.json(jsondepth - 1)
            if self.lote:
                json['lote'] = self.lote.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

