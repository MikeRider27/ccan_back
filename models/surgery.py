import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.patient import PatientModel
from models.hospital import HospitalModel


class SurgeryModel(BaseModel):
    __tablename__ = 'surgery'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id), nullable=False)
    date = db.Column(db.DateTime)
    observation = db.Column(db.String)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    surgical_technique = db.Column(db.String)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)
    medical_team = db.relationship('MedicalTeamModel', cascade="all, delete-orphan")

    def __init__(self, id, patient_id, date, observation, hospital_id,
                 date_create=None, user_create=None, date_modify=None, user_modify=None, surgical_technique=None):
        self.id = id
        self.patient_id = patient_id
        self.date = date
        self.observation = observation
        self.hospital_id = hospital_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.surgical_technique = surgical_technique

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
            'observation': self.observation,
            'hospital_id': self.hospital_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'surgical_technique': self.surgical_technique,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
            json['medical_team'] = []
            if self.medical_team:
                for doctor in self.medical_team:
                    json['medical_team'].append(doctor.json(jsondepth - 1))
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

