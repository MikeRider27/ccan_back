import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.hospital import HospitalModel
from models.patient import PatientModel


class PatientExclusionCriteriaModel(BaseModel):
    __tablename__ = 'patient_exclusion_criteria'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    distant_metastatic = db.Column(db.Boolean)
    life_expectancy_greater_5_comorbidities = db.Column(db.Boolean)
    fevi_less_50 = db.Column(db.Boolean)
    ecog_eq_greater_2 = db.Column(db.Boolean)
    congestive_ic = db.Column(db.Boolean)
    ischemic_heart_disease = db.Column(db.Boolean)
    arritmia_inestable = db.Column(db.Boolean)
    valve_disease = db.Column(db.Boolean)
    uncontrolled_hta = db.Column(db.Boolean)
    doxorubicin_greater_360mg_by_m2 = db.Column(db.Boolean)
    epirrubicina_greater_720mg_by_m2 = db.Column(db.Boolean)
    pregnancy = db.Column(db.Boolean)
    lactation = db.Column(db.Boolean)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def __init__(self, id, patient_id, distant_metastatic, life_expectancy_greater_5_comorbidities, fevi_less_50,
                 ecog_eq_greater_2, congestive_ic, ischemic_heart_disease, arritmia_inestable, valve_disease,
                 uncontrolled_hta, doxorubicin_greater_360mg_by_m2, epirrubicina_greater_720mg_by_m2, pregnancy,
                 lactation, date_create=None, user_create=None, date_modify=None, user_modify=None, hospital_id=None):
        self.id = id
        self.patient_id = patient_id
        self.distant_metastatic = distant_metastatic
        self.life_expectancy_greater_5_comorbidities = life_expectancy_greater_5_comorbidities
        self.fevi_less_50 = fevi_less_50
        self.ecog_eq_greater_2 = ecog_eq_greater_2
        self.congestive_ic = congestive_ic
        self.ischemic_heart_disease = ischemic_heart_disease
        self.arritmia_inestable = arritmia_inestable
        self.valve_disease = valve_disease
        self.uncontrolled_hta = uncontrolled_hta
        self.doxorubicin_greater_360mg_by_m2 = doxorubicin_greater_360mg_by_m2
        self.epirrubicina_greater_720mg_by_m2 = epirrubicina_greater_720mg_by_m2
        self.pregnancy = pregnancy
        self.lactation = lactation
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.hospital_id = hospital_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'distant_metastatic': self.distant_metastatic,
            'life_expectancy_greater_5_comorbidities': self.life_expectancy_greater_5_comorbidities,
            'fevi_less_50': self.fevi_less_50,
            'ecog_eq_greater_2': self.ecog_eq_greater_2,
            'congestive_ic': self.congestive_ic,
            'ischemic_heart_disease': self.ischemic_heart_disease,
            'arritmia_inestable': self.arritmia_inestable,
            'valve_disease': self.valve_disease,
            'uncontrolled_hta': self.uncontrolled_hta,
            'doxorubicin_greater_360mg_by_m2': self.doxorubicin_greater_360mg_by_m2,
            'epirrubicina_greater_720mg_by_m2': self.epirrubicina_greater_720mg_by_m2,
            'pregnancy': self.pregnancy,
            'lactation': self.lactation,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
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

    def patient_excluded(self):
        if self.distant_metastatic:
            return True
        if self.life_expectancy_greater_5_comorbidities:
            return True
        if self.fevi_less_50:
            return True
        if self.ecog_eq_greater_2:
            return True
        if self.congestive_ic:
            return True
        if self.ischemic_heart_disease:
            return True
        if self.arritmia_inestable:
            return True
        if self.valve_disease:
            return True
        if self.uncontrolled_hta:
            return True
        if self.doxorubicin_greater_360mg_by_m2:
            return True
        if self.epirrubicina_greater_720mg_by_m2:
            return True
        if self.pregnancy:
            return True
        if self.lactation:
            return True

        return False

