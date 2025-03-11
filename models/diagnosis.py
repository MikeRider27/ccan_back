import datetime

from db import db, BaseModel
from models.cie_o_morphology import CieOMorphologyModel
from models.cie_o_topography import CieOTopographyModel
from models.cie_o_tumor_location import CieOTumorLocationModel
from models.hospital import HospitalModel
from models.patient import PatientModel
from models.cie_10 import Cie_10Model


class DiagnosisModel(BaseModel):
    __tablename__ = 'diagnosis'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    codification_type = db.Column(db.String(10))
    cie_10_code_id = db.Column(db.BigInteger, db.ForeignKey(Cie_10Model.id))
    cie_o_morphology_id = db.Column(db.BigInteger, db.ForeignKey(CieOMorphologyModel.id))
    cie_o_topography_id = db.Column(db.BigInteger, db.ForeignKey(CieOTopographyModel.id))
    cie_o_tumor_location_id = db.Column(db.BigInteger, db.ForeignKey(CieOTumorLocationModel.id))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    cie_10 = db.relationship('Cie_10Model', foreign_keys=[cie_10_code_id], uselist=False)
    cie_o_morphology = db.relationship('CieOMorphologyModel', foreign_keys=[cie_o_morphology_id], uselist=False)
    cie_o_topography = db.relationship('CieOTopographyModel', foreign_keys=[cie_o_topography_id], uselist=False)
    cie_o_tumor_location = db.relationship('CieOTumorLocationModel', foreign_keys=[cie_o_tumor_location_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def __init__(self, id=None, patient_id=None, date=None, codification_type=None, cie_10_code_id=None,
                 cie_o_morphology_id=None, cie_o_topography_id=None, cie_o_tumor_location_id=None, date_create=None,
                 user_create=None, date_modify=None, user_modify=None, hospital_id=None):
        self.id = id
        self.patient_id = patient_id
        self.cie_10_code_id = cie_10_code_id
        self.cie_o_morphology_id = cie_o_morphology_id
        self.cie_o_topography_id = cie_o_topography_id
        self.cie_o_tumor_location_id = cie_o_tumor_location_id
        self.codification_type = codification_type
        self.date = date
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.hospital_id = hospital_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
            'codification_type': self.codification_type,
            'cie_10_code_id': self.cie_10_code_id,
            'cie_o_morphology_id': self.cie_o_morphology_id,
            'cie_o_topography_id': self.cie_o_topography_id,
            'cie_o_tumor_location_id': self.cie_o_tumor_location_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'hospital_id': self.hospital_id,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.cie_10:
                json['cie_10'] = self.cie_10.json(jsondepth - 1)
            if self.cie_o_morphology:
                json['cie_o_morphology'] = self.cie_o_morphology.json(jsondepth - 1)
            if self.cie_o_topography:
                json['cie_o_topography'] = self.cie_o_topography.json(jsondepth - 1)
            if self.cie_o_tumor_location:
                json['cie_o_tumor_location'] = self.cie_o_tumor_location.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

