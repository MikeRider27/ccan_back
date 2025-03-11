import base64
import datetime

from flask_restful.reqparse import Namespace
from sqlalchemy.ext.hybrid import hybrid_property

from db import db, BaseModel
from models.deposit_stock import DepositStockModel
from models.lot import LotModel
from models.medicine import MedicineModel
from models.patient import PatientModel, OriginsCode
from models.stock import StockModel


class DispatchMedicationsModel(BaseModel):
    __tablename__ = 'dispatch_medications'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    deposit_stock_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id), nullable=False)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id), nullable=False)
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    origin = db.Column(db.String(30), nullable=False, default='')
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    lote_id = db.Column(db.BigInteger, db.ForeignKey(LotModel.id))

    deposit_stock = db.relationship('DepositStockModel', foreign_keys=[deposit_stock_id], uselist=False)
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)
    lote = db.relationship('LotModel', foreign_keys=[lote_id], uselist=False)

    @hybrid_property
    def stock(self):
        stock = StockModel.query.filter_by(medicine_id=self.medicine_id).first()
        if not stock:
            return None
        return stock.json(1)

    def __init__(self, id=None, deposit_stock_id=None, patient_id=None, medicine_id=None, quantity=None, origin=None,
                 date_create=None, user_create=None, date=None, lote_id=None):
        self.id = id
        self.deposit_stock_id = deposit_stock_id
        self.patient_id = patient_id
        self.medicine_id = medicine_id
        self.quantity = quantity
        self.origin = origin
        self.date_create = date_create
        self.user_create = user_create
        self.date = date
        self.lote_id = lote_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'deposit_stock_id': self.deposit_stock_id,
            'patient_id': self.patient_id,
            'medicine_id': self.medicine_id,
            'quantity': self.quantity,
            'origin': self.origin,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'stock': self.stock,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
            'lote_id': self.lote_id,
        }

        if jsondepth > 0:
            if self.deposit_stock:
                json['deposit_stock'] = self.deposit_stock.json(jsondepth - 1)
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
            if self.lote:
                json['lote'] = self.lote.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

