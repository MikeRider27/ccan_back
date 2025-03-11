import base64
import datetime

from flask_restful.reqparse import Namespace
from sqlalchemy.dialects.sqlite import JSON

from db import db, BaseModel
from models.parameter import ParameterModel
from models.patient import PatientModel


class PatientInclusionCriteriaAdjuvantTrastuzumabModel(BaseModel):
    __tablename__ = 'patient_inclusion_criteria_adjuvant_trastuzumab'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    diagnosed_invasive_adenocarcinoma = db.Column(db.Boolean)
    adenocarcinoma_completely_resected = db.Column(db.Boolean)
    tumor_diameter_greater_10mm = db.Column(db.Boolean)
    adjuvant_trastuzumab_her2_positive = db.Column(db.Boolean)
    her2_positive_id = db.Column(JSON)
    determination_hormone_receptors = db.Column(db.Boolean)
    absolute_neutrophils_eq_greater_1500_ul = db.Column(db.Boolean)
    platelets_eq_greater_90000_mm3 = db.Column(db.Boolean)
    renal_hepatic_appropriate = db.Column(db.Boolean)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)

    def __init__(self, id=None, patient_id=None, diagnosed_invasive_adenocarcinoma=None,
                 adenocarcinoma_completely_resected=None, tumor_diameter_greater_10mm=None,
                 adjuvant_trastuzumab_her2_positive=None, her2_positive_id=None, determination_hormone_receptors=None,
                 absolute_neutrophils_eq_greater_1500_ul=None, platelets_eq_greater_90000_mm3=None,
                 renal_hepatic_appropriate=None):
        self.id = id
        self.patient_id = patient_id
        self.diagnosed_invasive_adenocarcinoma = diagnosed_invasive_adenocarcinoma
        self.adenocarcinoma_completely_resected = adenocarcinoma_completely_resected
        self.tumor_diameter_greater_10mm = tumor_diameter_greater_10mm
        self.adjuvant_trastuzumab_her2_positive = adjuvant_trastuzumab_her2_positive
        self.her2_positive_id = her2_positive_id
        self.determination_hormone_receptors = determination_hormone_receptors
        self.absolute_neutrophils_eq_greater_1500_ul = absolute_neutrophils_eq_greater_1500_ul
        self.platelets_eq_greater_90000_mm3 = platelets_eq_greater_90000_mm3
        self.renal_hepatic_appropriate = renal_hepatic_appropriate

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'diagnosed_invasive_adenocarcinoma': self.diagnosed_invasive_adenocarcinoma,
            'adenocarcinoma_completely_resected': self.adenocarcinoma_completely_resected,
            'tumor_diameter_greater_10mm': self.tumor_diameter_greater_10mm,
            'adjuvant_trastuzumab_her2_positive': self.adjuvant_trastuzumab_her2_positive,
            'her2_positive_id': self.her2_positive_id,
            'determination_hormone_receptors': self.determination_hormone_receptors,
            'absolute_neutrophils_eq_greater_1500_ul': self.absolute_neutrophils_eq_greater_1500_ul,
            'platelets_eq_greater_90000_mm3': self.platelets_eq_greater_90000_mm3,
            'renal_hepatic_appropriate': self.renal_hepatic_appropriate,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def patient_included(self):
        if not self.diagnosed_invasive_adenocarcinoma:
            return False
        if not self.adenocarcinoma_completely_resected:
            return False
        if not self.tumor_diameter_greater_10mm:
            return False
        if not self.adjuvant_trastuzumab_her2_positive:
            return False
        if not self.determination_hormone_receptors:
            return False
        if not self.absolute_neutrophils_eq_greater_1500_ul:
            return False
        if not self.platelets_eq_greater_90000_mm3:
            return False
        if not self.renal_hepatic_appropriate:
            return False

        return True

