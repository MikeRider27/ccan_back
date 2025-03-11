import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.medicine import MedicineModel
from models.chemotherapy import ChemotherapyModel


class MedicineChemotherapyModel(BaseModel):
    __tablename__ = 'medicine_chemotherapy'

    id = db.Column(db.BigInteger, primary_key=True)
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id))
    chemotherapy_id = db.Column(db.BigInteger, db.ForeignKey(ChemotherapyModel.id))
    quantity = db.Column(db.Numeric)
    observation = db.Column(db.String)
    dose = db.Column(db.Numeric)
    presentation = db.Column(db.String)
    concentration = db.Column(db.String)

    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)
    chemotherapy = db.relationship('ChemotherapyModel', foreign_keys=[chemotherapy_id], uselist=False)

    def __init__(self, id=None, medicine_id=None, chemotherapy_id=None, quantity=None, observation=None, dose=None, presentation=None, concentration=None):
        self.id = id
        self.medicine_id = medicine_id
        self.chemotherapy_id = chemotherapy_id
        self.quantity = quantity
        self.observation = observation
        self.dose = dose
        self.presentation = presentation
        self.concentration = concentration

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'chemotherapy_id': self.chemotherapy_id,
            'quantity': self.quantity,
            'observation': self.observation,
            'dose': self.dose,
            'presentation': self.presentation,
            'concentration': self.concentration,
        }

        if jsondepth > 0:
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
            if self.chemotherapy:
                json['chemotherapy'] = self.chemotherapy.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

