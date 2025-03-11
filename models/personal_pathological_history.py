import datetime

from db import db, BaseModel
from models.cie_10 import Cie_10Model
from models.hospital import HospitalModel
from models.menopausal_state import MenopausalStateModel
from models.parameter import ParameterModel
from models.patient import PatientModel


class PersonalPathologicalHistoryModel(BaseModel):
    __tablename__ = 'personal_pathological_history'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    family_members_with_cancer = db.Column(db.String)
    cie_10_code_id = db.Column(db.BigInteger, db.ForeignKey(Cie_10Model.id))
    observation = db.Column(db.String)
    app_funtional_class_nyha_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    app_ischemic_heart_disease = db.Column(db.Boolean)
    app_heart_failure = db.Column(db.Boolean)
    app_arrhythmia = db.Column(db.Boolean)
    app_heart_others = db.Column(db.Boolean)
    app_heart_others_input = db.Column(db.String)
    menopausal_state_id = db.Column(db.BigInteger, db.ForeignKey(MenopausalStateModel.id))
    app_menopausal_others = db.Column(db.String)
    fevi_percentage = db.Column(db.Integer)
    fevi_date = db.Column(db.DateTime)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id), nullable=False)

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    cie_10_code = db.relationship('Cie_10Model', foreign_keys=[cie_10_code_id], uselist=False)
    app_funtional_class_nyha = db.relationship('ParameterModel', foreign_keys=[app_funtional_class_nyha_id], uselist=False)
    menopausal_state = db.relationship('MenopausalStateModel', foreign_keys=[menopausal_state_id], uselist=False)
    family_list = db.relationship('PatientFamilyWithCancerModel', cascade="all, delete-orphan")
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)

    def __init__(self, id=None, patient_id=None, family_members_with_cancer=None, cie_10_code_id=None, observation=None, app_funtional_class_nyha_id=None,
                 app_ischemic_heart_disease=None, app_heart_failure=None, app_arrhythmia=None, app_heart_others=None,
                 app_heart_others_input=None, menopausal_state_id=None, app_menopausal_others=None,
                 fevi_percentage=None, fevi_date=None, date_create=None, user_create=None, date_modify=None,
                 user_modify=None, hospital_id=None):
        self.id = id
        self.patient_id = patient_id
        self.family_members_with_cancer = family_members_with_cancer
        self.cie_10_code_id = cie_10_code_id
        self.observation = observation
        self.app_funtional_class_nyha_id = app_funtional_class_nyha_id
        self.app_ischemic_heart_disease = app_ischemic_heart_disease
        self.app_heart_failure = app_heart_failure
        self.app_arrhythmia = app_arrhythmia
        self.app_heart_others = app_heart_others
        self.app_heart_others_input = app_heart_others_input
        self.menopausal_state_id = menopausal_state_id
        self.app_menopausal_others = app_menopausal_others
        self.fevi_percentage = fevi_percentage
        self.fevi_date = fevi_date
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.hospital_id = hospital_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'family_members_with_cancer': self.family_members_with_cancer,
            'cie_10_code_id': self.cie_10_code_id,
            'observation': self.observation,
            'app_ischemic_heart_disease': self.app_ischemic_heart_disease,
            'app_heart_failure': self.app_heart_failure,
            'app_arrhythmia': self.app_arrhythmia,
            'app_heart_others': self.app_heart_others,
            'app_heart_others_input': self.app_heart_others_input,
            'menopausal_state_id': self.menopausal_state_id,
            'app_menopausal_others': self.app_menopausal_others,
            'fevi_percentage': self.fevi_percentage,
            'fevi_date': self.fevi_date.strftime("%d/%m/%Y") if self.fevi_date else None,
            'date_create': self.date_create,
            'user_create': self.user_create,
            'date_modify': self.date_modify,
            'user_modify': self.user_modify,
            'hospital_id': self.hospital_id,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.cie_10_code:
                json['cie_10_code'] = self.cie_10_code.json(jsondepth - 1)
            if self.app_funtional_class_nyha:
                json['app_funtional_class_nyha'] = self.app_funtional_class_nyha.json(jsondepth - 1)
            if self.menopausal_state:
                json['menopausal_state'] = self.menopausal_state.json(jsondepth - 1)
            json['family_list'] = []
            if self.family_list:
                for family in self.family_list:
                    json['family_list'].append(family.json(jsondepth - 1))
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

