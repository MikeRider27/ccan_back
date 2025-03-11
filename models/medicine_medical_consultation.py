import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.medicine import MedicineModel
from models.medical_consultation import MedicalConsultationModel


class MedicineMedicalConsultationModel(BaseModel):
    __tablename__ = 'medicine_medical_consultation'

    id = db.Column(db.BigInteger, primary_key=True)
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id))
    medical_consultation_id = db.Column(db.BigInteger, db.ForeignKey(MedicalConsultationModel.id))
    quantity = db.Column(db.Numeric)
    observation = db.Column(db.String)
    dose = db.Column(db.Numeric)
    presentation = db.Column(db.String)
    concentration = db.Column(db.String)

    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)
    medical_consultation = db.relationship('MedicalConsultationModel', foreign_keys=[medical_consultation_id], uselist=False)

    def __init__(self, id=None, medicine_id=None, medical_consultation_id=None, quantity=None, observation=None,
                 dose=None, presentation=None, concentration=None):
        self.id = id
        self.medicine_id = medicine_id
        self.medical_consultation_id = medical_consultation_id
        self.quantity = quantity
        self.observation = observation
        self.dose = dose
        self.presentation = presentation
        self.concentration = concentration

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'medical_consultation_id': self.medical_consultation_id,
            'quantity': self.quantity,
            'observation': self.observation,
            'dose': self.dose,
            'presentation': self.presentation,
            'concentration': self.concentration,
        }

        if jsondepth > 0:
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
            if self.medical_consultation:
                json['medical_consultation'] = self.medical_consultation.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

