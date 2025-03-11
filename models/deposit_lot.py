import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.deposit_stock import DepositStockModel
from models.lot import LotModel
from models.medicine import MedicineModel


class DepositLotModel(BaseModel):
    __tablename__ = 'deposit_lot'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    deposit_stock_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id))
    lote_id = db.Column(db.BigInteger, db.ForeignKey(LotModel.id))
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id))
    quantity = db.Column(db.INTEGER)

    deposit_stock = db.relationship('DepositStockModel', foreign_keys=[deposit_stock_id], uselist=False)
    lote = db.relationship('LotModel', foreign_keys=[lote_id], uselist=False)
    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)

    def __init__(self, id=None, deposit_stock_id=None, lote_id=None, medicine_id=None, quantity=None):
        self.id = id
        self.deposit_stock_id = deposit_stock_id
        self.lote_id = lote_id
        self.medicine_id = medicine_id
        self.quantity = quantity

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'deposit_stock_id': self.deposit_stock_id,
            'lote_id': self.lote_id,
            'medicine_id': self.medicine_id,
            'quantity': self.quantity,
        }

        if jsondepth > 0:
            if self.deposit_stock:
                json['deposit_stock'] = self.deposit_stock.json(jsondepth - 1)
            if self.lote:
                json['lote'] = self.lote.json(jsondepth - 1)
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

