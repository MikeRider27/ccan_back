import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.doctor import DoctorModel
from models.hospital import HospitalModel
from models.patient import PatientModel
from models.patient_inclusion_criteria_adjuvant_trastuzumab import PatientInclusionCriteriaAdjuvantTrastuzumabModel
from models.patient_inclusion_criteria_neoadjuvant_trastuzumab import PatientInclusionCriteriaNeoadjuvantTrastuzumabModel
from models.specialty import SpecialtyModel


class PatientInclusionCriteriaModel(BaseModel):
    __tablename__ = 'patient_inclusion_criteria'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    treatment_type = db.Column(db.String(30))
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    specialty_id = db.Column(db.BigInteger, db.ForeignKey(SpecialtyModel.id))
    patient_inclusion_criteria_adjuvant_id = db.Column(db.BigInteger, db.ForeignKey(PatientInclusionCriteriaAdjuvantTrastuzumabModel.id))
    patient_inclusion_criteria_neoadjuvant_id = db.Column(db.BigInteger, db.ForeignKey(PatientInclusionCriteriaNeoadjuvantTrastuzumabModel.id))
    has_signed_informed_consent = db.Column(db.Boolean)
    patient_received_document = db.Column(db.Boolean)
    consent_obtained_through_dialogue = db.Column(db.Boolean)
    has_received_sufficient_sufficient = db.Column(db.Boolean)
    has_asked_questions_and_can_continue_asking = db.Column(db.Boolean)
    informed_receive_permanent_continuous_information = db.Column(db.Boolean)
    information_received_clear_complete = db.Column(db.Boolean)
    received_information_understandable_language = db.Column(db.Boolean)
    treatment_hospital_id = db.Column(db.BigInteger)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    patient_inclusion_criteria_adjuvant = db.relationship('PatientInclusionCriteriaAdjuvantTrastuzumabModel', foreign_keys=[patient_inclusion_criteria_adjuvant_id], uselist=False)
    patient_inclusion_criteria_neoadjuvant = db.relationship('PatientInclusionCriteriaNeoadjuvantTrastuzumabModel', foreign_keys=[patient_inclusion_criteria_neoadjuvant_id], uselist=False)
    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)
    specialty = db.relationship('SpecialtyModel', foreign_keys=[specialty_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def __init__(self, id, patient_id, treatment_type, patient_inclusion_criteria_adjuvant_id,
                 patient_inclusion_criteria_neoadjuvant_id, has_signed_informed_consent, patient_received_document,
                 consent_obtained_through_dialogue, has_received_sufficient_sufficient,
                 has_asked_questions_and_can_continue_asking, informed_receive_permanent_continuous_information,
                 information_received_clear_complete, received_information_understandable_language,
                 treatment_hospital_id, doctor_id=None, specialty_id=None,
                 date_create=None, user_create=None, date_modify=None, user_modify=None, hospital_id=None):
        self.id = id
        self.patient_id = patient_id
        self.treatment_type = treatment_type
        self.doctor_id = doctor_id
        self.specialty_id = specialty_id
        self.patient_inclusion_criteria_adjuvant_id = patient_inclusion_criteria_adjuvant_id
        self.patient_inclusion_criteria_neoadjuvant_id = patient_inclusion_criteria_neoadjuvant_id
        self.has_signed_informed_consent = has_signed_informed_consent
        self.patient_received_document = patient_received_document
        self.consent_obtained_through_dialogue = consent_obtained_through_dialogue
        self.has_received_sufficient_sufficient = has_received_sufficient_sufficient
        self.has_asked_questions_and_can_continue_asking = has_asked_questions_and_can_continue_asking
        self.informed_receive_permanent_continuous_information = informed_receive_permanent_continuous_information
        self.information_received_clear_complete = information_received_clear_complete
        self.received_information_understandable_language = received_information_understandable_language
        self.treatment_hospital_id = treatment_hospital_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.hospital_id = hospital_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'treatment_type': self.treatment_type,
            'doctor_id': self.doctor_id,
            'specialty_id': self.specialty_id,
            'patient_inclusion_criteria_adjuvant_id': self.patient_inclusion_criteria_adjuvant_id,
            'patient_inclusion_criteria_neoadjuvant_id': self.patient_inclusion_criteria_neoadjuvant_id,
            'has_signed_informed_consent': self.has_signed_informed_consent,
            'patient_received_document': self.patient_received_document,
            'consent_obtained_through_dialogue': self.consent_obtained_through_dialogue,
            'has_received_sufficient_sufficient': self.has_received_sufficient_sufficient,
            'has_asked_questions_and_can_continue_asking': self.has_asked_questions_and_can_continue_asking,
            'informed_receive_permanent_continuous_information': self.informed_receive_permanent_continuous_information,
            'information_received_clear_complete': self.information_received_clear_complete,
            'received_information_understandable_language': self.received_information_understandable_language,
            'treatment_hospital_id': self.treatment_hospital_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'hospital_id': self.hospital_id,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.patient_inclusion_criteria_adjuvant:
                json['patient_inclusion_criteria_adjuvant'] = self.patient_inclusion_criteria_adjuvant.json(jsondepth - 1)
            if self.patient_inclusion_criteria_neoadjuvant:
                json['patient_inclusion_criteria_neoadjuvant'] = self.patient_inclusion_criteria_neoadjuvant.json(jsondepth - 1)
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
            if self.specialty:
                json['specialty'] = self.specialty.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

