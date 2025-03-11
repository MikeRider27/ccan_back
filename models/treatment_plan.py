import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from db import db, BaseModel
from models.cie_10 import Cie_10Model
from models.cie_o_morphology import CieOMorphologyModel
from models.cie_o_topography import CieOTopographyModel
from models.cie_o_tumor_location import CieOTumorLocationModel
from models.doctor import DoctorModel
from models.hospital import HospitalModel
from models.parameter import ParameterModel
from models.patient import PatientModel, OriginsCode
from models.periodicity import PeriodicityModel
from models.type_treatment import TypeTreatmentModel


class TreatmentPlanModel(BaseModel):
    __tablename__ = 'treatment_plan'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id))
    date = db.Column(db.DateTime)
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    size = db.Column(db.Numeric)
    weight = db.Column(db.Numeric)
    sc = db.Column(db.Numeric)
    medical_visit_observation = db.Column(db.String)
    cie_10_code_id = db.Column(db.BigInteger, db.ForeignKey(Cie_10Model.id))
    cie_o_morphology_id = db.Column(db.BigInteger, db.ForeignKey(CieOMorphologyModel.id))
    cie_o_topography_id = db.Column(db.BigInteger, db.ForeignKey(CieOTopographyModel.id))
    cie_o_tumor_location_id = db.Column(db.BigInteger, db.ForeignKey(CieOTumorLocationModel.id))
    type_id = db.Column(db.BigInteger, db.ForeignKey(TypeTreatmentModel.id))
    number_sessions = db.Column(db.Integer)
    periodicity_id = db.Column(db.BigInteger, db.ForeignKey(PeriodicityModel.id))
    date_first_cycle = db.Column(db.Date)
    date_last_cycle = db.Column(db.Date)
    observation = db.Column(db.String)
    origin = db.Column(db.String, default=OriginsCode.CCAN_CITY_SOFT.value)
    date_create = db.Column(db.DateTime, default=datetime.datetime.now)
    user_create = db.Column(db.String(30))
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    number = db.Column(db.Numeric)
    state_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)
    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)
    cie_10 = db.relationship('Cie_10Model', foreign_keys=[cie_10_code_id], uselist=False)
    cie_o_morphology = db.relationship('CieOMorphologyModel', foreign_keys=[cie_o_morphology_id], uselist=False)
    cie_o_topography = db.relationship('CieOTopographyModel', foreign_keys=[cie_o_topography_id], uselist=False)
    cie_o_tumor_location = db.relationship('CieOTumorLocationModel', foreign_keys=[cie_o_tumor_location_id], uselist=False)
    type_treatment = db.relationship('TypeTreatmentModel', foreign_keys=[type_id], uselist=False)
    periodicity = db.relationship('PeriodicityModel', foreign_keys=[periodicity_id], uselist=False)
    medicine_list = db.relationship('MedicineTreatmentPlanModel', cascade="all, delete-orphan")
    state = db.relationship('ParameterModel', foreign_keys=[state_id], uselist=False)

    chemotherapy_sessions = db.relationship('ChemotherapyModel', secondary='chemotherapy_treatment_plan')
    radiotherapy_sessions = db.relationship('RadiotherapyModel', secondary='radiotherapy_treatment_plan')

    @hybrid_property
    def get_number_sessions(self):
        number_sessions = None
        if self.type_treatment.code == 'CHEMOTHERAPY':
            number_sessions = len(self.chemotherapy_sessions)

        if self.type_treatment.code == 'RADIOTHERAPY':
            number_sessions = len(self.radiotherapy_sessions)

        return number_sessions

    def __init__(self, id, patient_id, hospital_id, date, doctor_id, size, weight, sc,
                 medical_visit_observation, cie_10_code_id, cie_o_morphology_id,
                 cie_o_topography_id, cie_o_tumor_location_id, type_id, number_sessions, periodicity_id,
                 date_first_cycle, date_last_cycle, observation, origin, date_create=None, user_create=None, date_modify=None,
                 user_modify=None, number=None, state_id=None):
        self.id = id
        self.patient_id = patient_id
        self.hospital_id = hospital_id
        self.date = date
        self.doctor_id = doctor_id
        self.size = size
        self.weight = weight
        self.sc = sc
        self.medical_visit_observation = medical_visit_observation
        self.cie_10_code_id = cie_10_code_id
        self.cie_o_morphology_id = cie_o_morphology_id
        self.cie_o_topography_id = cie_o_topography_id
        self.cie_o_tumor_location_id = cie_o_tumor_location_id
        self.type_id = type_id
        self.number_sessions = number_sessions
        self.periodicity_id = periodicity_id
        self.date_first_cycle = date_first_cycle
        self.date_last_cycle = date_last_cycle
        self.observation = observation
        self.origin = origin
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.number = number
        self.state_id = state_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
            'doctor_id': self.doctor_id,
            'size': self.size,
            'weight': self.weight,
            'sc': self.sc,
            'medical_visit_observation': self.medical_visit_observation,
            'cie_10_code_id': self.cie_10_code_id,
            'cie_o_morphology_id': self.cie_o_morphology_id,
            'cie_o_topography_id': self.cie_o_topography_id,
            'cie_o_tumor_location_id': self.cie_o_tumor_location_id,
            'type_id': self.type_id,
            'number_sessions': self.number_sessions,
            'periodicity_id': self.periodicity_id,
            'date_first_cycle': self.date_first_cycle.strftime("%d/%m/%Y") if self.date_first_cycle else None,
            'date_last_cycle': self.date_last_cycle.strftime("%d/%m/%Y") if self.date_last_cycle else None,
            'observation': self.observation,
            'origin': self.origin,
            'date_create': self.date_create,
            'user_create': self.user_create,
            'date_modify': self.date_modify,
            'user_modify': self.user_modify,
            'number': self.number,
            'state_id': self.state_id,
            'sessions': self.get_number_sessions
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
            if self.cie_10:
                json['cie_10'] = self.cie_10.json(jsondepth - 1)
            if self.cie_o_morphology:
                json['cie_o_morphology'] = self.cie_o_morphology.json(jsondepth - 1)
            if self.cie_o_topography:
                json['cie_o_topography'] = self.cie_o_topography.json(jsondepth - 1)
            if self.cie_o_tumor_location:
                json['cie_o_tumor_location'] = self.cie_o_tumor_location.json(jsondepth - 1)
            if self.type_treatment:
                json['type_treatment'] = self.type_treatment.json(jsondepth - 1)
            if self.periodicity:
                json['periodicity'] = self.periodicity.json(jsondepth - 1)
            json['medicine_list'] = []
            if self.medicine_list:
                for medicine in self.medicine_list:
                    json['medicine_list'].append(medicine.json(jsondepth - 1))
            if self.state:
                json['state'] = self.state.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

