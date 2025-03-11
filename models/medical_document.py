import base64
import datetime
import os

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.hospital import HospitalModel
from models.patient import PatientModel
from models.medical_document_type import MedicalDocumentTypeModel


class MedicalDocumentModel(BaseModel):
    __tablename__ = 'medical_document'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String)
    path = db.Column(db.String, nullable=False)
    medical_document_type_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentTypeModel.id), nullable=False)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id), nullable=False)
    modulo = db.Column(db.String)
    origen_id = db.Column(db.BigInteger)
    study_date = db.Column(db.DateTime)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    medical_document_type = db.relationship('MedicalDocumentTypeModel', foreign_keys=[medical_document_type_id],
                                            uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def __init__(self, id=None, description=None, path=None, medical_document_type_id=None, patient_id=None,
                 modulo=None, origen_id=None, study_date=None, date_create=None, user_create=None, date_modify=None,
                 user_modify=None, hospital_id=None):
        self.id = id
        self.description = description
        self.path = path
        self.patient_id = patient_id
        self.medical_document_type_id = medical_document_type_id
        self.modulo = modulo
        self.origen_id = origen_id
        self.study_date = study_date
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.hospital_id = hospital_id

    def json(self, jsondepth=0):
        path, file = os.path.split(self.path)
        json = {
            'id': self.id,
            'description': self.description,
            'path': self.path,
            'patient_id': self.patient_id,
            'medical_document_type_id': self.medical_document_type_id,
            'file_name': file,
            'modulo': self.modulo,
            'origen_id': self.origen_id,
            'study_date': self.study_date.strftime("%d/%m/%Y") if self.study_date else None,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'hospital_id': self.hospital_id,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.medical_document_type:
                json['medical_document_type'] = self.medical_document_type.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

