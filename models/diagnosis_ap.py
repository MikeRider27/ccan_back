import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.cie_10 import Cie_10Model
from models.cie_o_morphology import CieOMorphologyModel
from models.cie_o_topography import CieOTopographyModel
from models.cie_o_tumor_location import CieOTumorLocationModel
from models.doctor import DoctorModel
from models.parameter import ParameterModel
from models.patient import PatientModel, OriginsCode
from models.hospital import HospitalModel


class DiagnosisApModel(BaseModel):
    __tablename__ = 'diagnosis_ap'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    observation = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    tumor_size = db.Column(db.Numeric)
    cie_o_morphology_id = db.Column(db.BigInteger, db.ForeignKey(CieOMorphologyModel.id))
    cie_o_topography_id = db.Column(db.BigInteger, db.ForeignKey(CieOTopographyModel.id))
    cie_o_tumor_location_id = db.Column(db.BigInteger, db.ForeignKey(CieOTumorLocationModel.id))
    armpit_node_number = db.Column(db.Integer)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    armpit = db.Column(db.String(20))
    re = db.Column(db.String(20))
    rp = db.Column(db.String(20))
    her2 = db.Column(db.String(20))
    her2_positive_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    general_report = db.Column(db.String)
    origin = db.Column(db.String, default=OriginsCode.CCAN_CITY_SOFT.value)
    dx_presuntivo = db.Column(db.String)
    material = db.Column(db.String)
    diagnostico = db.Column(db.String)
    clasificacion = db.Column(db.String)
    macroscopia = db.Column(db.String)
    microscopia = db.Column(db.String)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)
    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)
    cie_o_morphology = db.relationship('CieOMorphologyModel', foreign_keys=[cie_o_morphology_id], uselist=False)
    cie_o_topography = db.relationship('CieOTopographyModel', foreign_keys=[cie_o_topography_id], uselist=False)
    cie_o_tumor_location = db.relationship('CieOTumorLocationModel', foreign_keys=[cie_o_tumor_location_id], uselist=False)
    her2_positive = db.relationship('ParameterModel', foreign_keys=[her2_positive_id], uselist=False)

    def __init__(self, id=None, observation=None, date=None, tumor_size=None, cie_o_morphology_id=None,
                 cie_o_topography_id=None, cie_o_tumor_location_id=None, armpit_node_number=None, patient_id=None,
                 hospital_id=None, doctor_id=None, date_create=None, user_create=None, date_modify=None,
                 user_modify=None, armpit=None, re=None, rp=None, her2=None, her2_positive_id=None, general_report=None,
                 origin=None, dx_presuntivo=None, material=None, diagnostico=None, clasificacion=None, macroscopia=None,
                 microscopia=None):
        self.id = id
        self.observation = observation
        self.date = date
        self.tumor_size = tumor_size
        self.cie_o_morphology_id = cie_o_morphology_id
        self.cie_o_topography_id = cie_o_topography_id
        self.cie_o_tumor_location_id = cie_o_tumor_location_id
        self.armpit_node_number = armpit_node_number
        self.patient_id = patient_id
        self.hospital_id = hospital_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.doctor_id = doctor_id
        self.armpit = armpit
        self.re = re
        self.rp = rp
        self.her2 = her2
        self.her2_positive_id = her2_positive_id
        self.general_report = general_report
        self.origin = origin
        self.dx_presuntivo = dx_presuntivo
        self.material = material
        self.diagnostico = diagnostico
        self.clasificacion = clasificacion
        self.macroscopia = macroscopia
        self.microscopia = microscopia

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'observation': self.observation,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
            'tumor_size': self.tumor_size,
            'cie_o_morphology_id': self.cie_o_morphology_id,
            'cie_o_topography_id': self.cie_o_topography_id,
            'cie_o_tumor_location_id': self.cie_o_tumor_location_id,
            'armpit_node_number': self.armpit_node_number,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'doctor_id': self.doctor_id,
            'armpit': self.armpit,
            're': self.re,
            'rp': self.rp,
            'her2': self.her2,
            'her2_positive_id': self.her2_positive_id,
            'general_report': self.general_report,
            'origin': self.origin,
            'dx_presuntivo': self.dx_presuntivo,
            'material': self.material,
            'diagnostico': self.diagnostico,
            'clasificacion': self.clasificacion,
            'macroscopia': self.macroscopia,
            'microscopia': self.microscopia,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
            if self.cie_o_morphology:
                json['cie_o_morphology'] = self.cie_o_morphology.json(jsondepth - 1)
            if self.cie_o_topography:
                json['cie_o_topography'] = self.cie_o_topography.json(jsondepth - 1)
            if self.cie_o_tumor_location:
                json['cie_o_tumor_location'] = self.cie_o_tumor_location.json(jsondepth - 1)
            if self.her2_positive:
                json['her2_positive'] = self.her2_positive.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

