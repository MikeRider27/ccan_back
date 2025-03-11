import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.deposit_stock import DepositStockModel
from models.medicine import MedicineModel
from models.treatment_follow_up import TreatmentFollowUpModel


class MedicineTreatmentFollowUpModel(BaseModel):
    __tablename__ = 'medicine_treatment_follow_up'

    id = db.Column(db.BigInteger, primary_key=True)
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id))
    treatment_follow_up_id = db.Column(db.BigInteger, db.ForeignKey(TreatmentFollowUpModel.id))
    quantity = db.Column(db.Float)
    observation = db.Column(db.String)
    dose = db.Column(db.Numeric)
    presentation = db.Column(db.String)
    concentration = db.Column(db.String)
    deposit_stock_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id))

    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)
    treatment_follow_up = db.relationship('TreatmentFollowUpModel', foreign_keys=[treatment_follow_up_id], uselist=False)
    deposit_stock = db.relationship('DepositStockModel', foreign_keys=[deposit_stock_id], uselist=False)

    def __init__(self, id=None, medicine_id=None, treatment_follow_up_id=None, quantity=None, observation=None, dose=None, presentation=None, concentration=None, deposit_stock_id=None):
        self.id = id
        self.medicine_id = medicine_id
        self.treatment_follow_up_id = treatment_follow_up_id
        self.quantity = quantity
        self.observation = observation
        self.dose = dose
        self.presentation = presentation
        self.concentration = concentration
        self.deposit_stock_id = deposit_stock_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'treatment_follow_up_id': self.treatment_follow_up_id,
            'quantity': self.quantity,
            'observation': self.observation,
            'dose': self.dose,
            'presentation': self.presentation,
            'concentration': self.concentration,
            'deposit_stock_id': self.deposit_stock_id
        }

        if jsondepth > 0:
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
            if self.treatment_follow_up:
                json['treatment_follow_up'] = self.treatment_follow_up.json(jsondepth - 1)
            if self.deposit_stock:
                json['deposit_stock'] = self.deposit_stock.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

