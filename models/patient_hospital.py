import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.patient import PatientModel
from models.hospital import HospitalModel


class PatientHospitalModel(BaseModel):
    __tablename__ = 'patient_hospital'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id))

    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def __init__(self, id=None, patient_id=None, hospital_id=None):
        self.id = id
        self.patient_id = patient_id
        self.hospital_id = hospital_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

