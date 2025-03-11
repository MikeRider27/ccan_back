import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.entries import EntriesModel
from models.medicine import MedicineModel
from models.parameter import ParameterModel


class StockModel(BaseModel):
    __tablename__ = 'stock'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    state_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id), nullable=False)

    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)
    state = db.relationship('ParameterModel', foreign_keys=[state_id], uselist=False)
    deposits = db.relationship('DepositStockModel')
    deposit_stock_list = db.relationship('DepositStockModel', back_populates='stock')
    entries_list = db.relationship(
        EntriesModel,
        secondary='inventory.entries_deposit_stock',
        primaryjoin="StockModel.id == EntriesDepositStockModel.deposit_stock_id",
        secondaryjoin="EntriesModel.id == EntriesDepositStockModel.entries_id"
    )

    def __init__(self, id=None, medicine_id=None, quantity=None, state_id=None):
        self.id = id
        self.medicine_id = medicine_id
        self.quantity = quantity
        self.state_id = state_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'quantity': self.quantity,
        }

        if jsondepth > 0:
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
            if self.state:
                json['state'] = self.state.json(jsondepth - 1)
            json['deposits'] = []
            if self.deposits:
                for deposit in self.deposits:
                    json['deposits'].append(deposit.json(jsondepth - 1))
            json['entries_list'] = []
            if self.entries_list:
                for entries in self.entries_list:
                    json['entries_list'].append(entries.json(jsondepth - 1))
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

