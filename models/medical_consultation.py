import datetime

from db import db, BaseModel
from models.cie_10 import Cie_10Model
from models.dispatch_medications import DispatchMedicationsModel
from models.doctor import DoctorModel
from models.hospital import HospitalModel
from models.parameter import ParameterModel
from models.patient import PatientModel, OriginsCode


class MedicalConsultationModel(BaseModel):
    __tablename__ = 'medical_consultation'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    date_first_diagnosis = db.Column(db.Date)
    diagnosis_by_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    observation = db.Column(db.String)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    date_consultation = db.Column(db.Date, default=datetime.datetime.now)
    cie_10_id = db.Column(db.BigInteger, db.ForeignKey(Cie_10Model.id))
    responsible_doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    apply_chemotherapy = db.Column(db.String(20))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)
    origin = db.Column(db.String, default='')

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    parameter = db.relationship('ParameterModel', foreign_keys=[diagnosis_by_id], uselist=False)
    cie_10 = db.relationship('Cie_10Model', foreign_keys=[cie_10_id], uselist=False)
    responsible_doctor = db.relationship('DoctorModel', foreign_keys=[responsible_doctor_id], uselist=False)
    medicine_list = db.relationship('MedicineMedicalConsultationModel', cascade="all, delete-orphan")
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def get_fuente(self):
        patient_origin = PatientModel.query.filter_by(id=self.patient_id, origin='SIGAP').first()
        dispatch_medicaments_origin = DispatchMedicationsModel.query.filter_by(patient_id=self.patient_id, origin='SICIAP').first()
        origins = set()
        if patient_origin:
            origins.add(patient_origin.origin)
        if self.origin == 'HIS':
            origins.add(self.origin)
        if dispatch_medicaments_origin:
            origins.add(dispatch_medicaments_origin.origin)
        return list(origins) if origins else None

    def __init__(self, id=None, patient_id=None, date_first_diagnosis=None, diagnosis_by_id=None,
                 observation=None, date_create=None, user_create=None, date_modify=None,
                 user_modify=None, date_consultation=None, cie_10_id=None, responsible_doctor_id=None,
                 apply_chemotherapy=None, hospital_id=None, origin=None):
        self.id = id
        self.patient_id = patient_id
        self.date_first_diagnosis = date_first_diagnosis
        self.diagnosis_by_id = diagnosis_by_id
        self.observation = observation
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.date_consultation = date_consultation
        self.cie_10_id = cie_10_id
        self.responsible_doctor_id = responsible_doctor_id
        self.apply_chemotherapy = apply_chemotherapy
        self.hospital_id = hospital_id
        self.origin = origin

    def get_dispatch_medications_by_patient(self):
        dispatches = DispatchMedicationsModel.query.filter_by(patient_id=self.patient_id).all()
        return dispatches
    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'date_first_diagnosis': self.date_first_diagnosis.strftime(
                "%d/%m/%Y") if self.date_first_diagnosis else None,
            'diagnosis_by_id': self.diagnosis_by_id,
            'observation': self.observation,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'date_consultation': self.date_consultation.strftime("%d/%m/%Y") if self.date_consultation else None,
            'cie_10_id': self.cie_10_id,
            'responsible_doctor_id': self.responsible_doctor_id,
            'apply_chemotherapy': self.apply_chemotherapy,
            'hospital_id': self.hospital_id,
            'origin': self.get_fuente(),
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.parameter:
                json['diagnosis_by'] = self.parameter.json(jsondepth - 1)
            if self.cie_10:
                json['cie_10'] = self.cie_10.json(jsondepth - 1)
            if self.responsible_doctor:
                json['responsible_doctor'] = self.responsible_doctor.json(jsondepth - 1)
            json['medicine_list'] = []
            if self.medicine_list:
                for medicine in self.medicine_list:
                    json['medicine_list'].append(medicine.json(jsondepth - 1))
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
            dispatch_meds = self.get_dispatch_medications_by_patient()
            if dispatch_meds:
                json['dispatch_medicine_list'] = [dispatch.json(jsondepth - 1) for dispatch in dispatch_meds]

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
