import datetime

from db import db, BaseModel
from models.doctor import DoctorModel
from models.hospital import HospitalModel
from models.parameter import ParameterModel
from models.patient import PatientModel


class RadiotherapyModel(BaseModel):
    __tablename__ = 'radiotherapy'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)
    nro_session = db.Column(db.Integer)
    observation = db.Column(db.Text)
    session_state_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    technician = db.Column(db.String)
    nurse = db.Column(db.String)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)
    session_state = db.relationship('ParameterModel', foreign_keys=[session_state_id], uselist=False)
    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)
    treatment_plan_list = db.relationship('RadiotherapyTreatmentPlanModel', cascade="all, delete-orphan")

    def __init__(self, id, date, patient_id, hospital_id, nro_session, observation, session_state_id,
                 date_create=None, user_create=None, date_modify=None, user_modify=None, doctor_id=None,
                 technician=None, nurse=None):
        self.id = id
        self.date = date
        self.patient_id = patient_id
        self.hospital_id = hospital_id
        self.nro_session = nro_session
        self.observation = observation
        self.session_state_id = session_state_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.doctor_id = doctor_id
        self.technician = technician
        self.nurse = nurse

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'date': self.date.strftime("%d/%m/%Y") if self.date else None,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
            'nro_session': self.nro_session,
            'observation': self.observation,
            'session_state_id': self.session_state_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'doctor_id': self.doctor_id,
            'technician': self.technician,
            'nurse': self.nurse,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
            if self.session_state:
                json['session_state'] = self.session_state.json(jsondepth - 1)
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
            json['treatment_plan_list'] = [
                {
                    'id': x.id,
                    'treatment_plan': x.treatment_plan.json(1),
                    'treatment_plan_id': x.treatment_plan_id,
                    'radiotherapy_id': x.radiotherapy_id,
                    'num_session': x.num_session
                } for x in self.treatment_plan_list] if self.treatment_plan_list else []
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
