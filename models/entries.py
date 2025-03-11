import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.deposit import DepositModel
from models.lot import LotModel
from models.medicine import MedicineModel
from models.manufacturer import ManufacturerModel
from models.patient import OriginsCode
from models.supplier import SupplierModel


class EntriesModel(BaseModel):
    __tablename__ = 'entries'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    deposit_id = db.Column(db.BigInteger, db.ForeignKey(DepositModel.id))
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id))
    description = db.Column(db.String(500))
    expiration_date = db.Column(db.DateTime)
    quantity = db.Column(db.Float)
    manufacturer_id = db.Column(db.BigInteger, db.ForeignKey(ManufacturerModel.id))
    manufacturing_date = db.Column(db.DateTime)
    supplier_id = db.Column(db.BigInteger, db.ForeignKey(SupplierModel.id))
    storage_conditions = db.Column(db.String(500))
    observation = db.Column(db.String(500))
    date = db.Column(db.DateTime, nullable=False)
    origin = db.Column(db.String(30), nullable=False, default=OriginsCode.CCAN_CITY_SOFT.value)
    lote_id = db.Column(db.BigInteger, db.ForeignKey(LotModel.id))

    deposit = db.relationship('DepositModel', foreign_keys=[deposit_id], uselist=False)
    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)
    manufacturer = db.relationship('ManufacturerModel', foreign_keys=[manufacturer_id], uselist=False)
    supplier = db.relationship('SupplierModel', foreign_keys=[supplier_id], uselist=False)
    lote = db.relationship('LotModel', foreign_keys=[lote_id], uselist=False)

    def __init__(self, id=None, deposit_id=None, medicine_id=None, description=None, expiration_date=None,
                 quantity=None, manufacturer_id=None, manufacturing_date=None, supplier_id=None,
                 storage_conditions=None, observation=None, date=None, origin=None, lote_id=None):
        self.id = id
        self.deposit_id = deposit_id
        self.medicine_id = medicine_id
        self.description = description
        self.expiration_date = expiration_date
        self.quantity = quantity
        self.manufacturer_id = manufacturer_id
        self.manufacturing_date = manufacturing_date
        self.supplier_id = supplier_id
        self.storage_conditions = storage_conditions
        self.observation = observation
        self.date = date
        self.origin = origin
        self.lote_id = lote_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'expiration_date': self.expiration_date.strftime("%d/%m/%Y") if self.expiration_date else None,
            'quantity': self.quantity,
            'manufacturing_date': self.manufacturing_date.strftime("%d/%m/%Y") if self.manufacturing_date else None,
            'storage_conditions': self.storage_conditions,
            'observation': self.observation,
            'deposit_id': self.deposit_id,
            'medicine_id': self.medicine_id,
            'manufacturer_id': self.manufacturer_id,
            'supplier_id': self.supplier_id,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
            'origin': self.origin,
            'lote_id': self.lote_id
        }

        if jsondepth > 0:
            # if self.lot:
            #     json['lot'] = self.lot.json(jsondepth - 1)
            if self.deposit:
                json['deposit'] = self.deposit.json(jsondepth - 1)
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
            if self.manufacturer:
                json['manufacturer'] = self.manufacturer.json(jsondepth - 1)
            if self.supplier:
                json['supplier'] = self.supplier.json(jsondepth - 1)
            if self.lote:
                json['lote'] = self.lote.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

