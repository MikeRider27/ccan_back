import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.personal_pathological_history import PersonalPathologicalHistoryModel
from models.parameter import ParameterModel


class PatientFamilyWithCancerModel(BaseModel):
    __tablename__ = 'patient_family_with_cancer'

    id = db.Column(db.BigInteger, primary_key=True)
    personal_pathological_history_id = db.Column(db.BigInteger, db.ForeignKey(PersonalPathologicalHistoryModel.id))
    family_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    family_vital_state_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    cancer_type = db.Column(db.String)

    personal_pathological_history = db.relationship('PersonalPathologicalHistoryModel', foreign_keys=[personal_pathological_history_id], uselist=False)
    family = db.relationship('ParameterModel', foreign_keys=[family_id], uselist=False)
    family_vital_state = db.relationship('ParameterModel', foreign_keys=[family_vital_state_id], uselist=False)

    def __init__(self, id=None, personal_pathological_history_id=None, family_id=None, family_vital_state_id=None,
                 cancer_type=None):
        self.id = id
        self.personal_pathological_history_id = personal_pathological_history_id
        self.family_id = family_id
        self.family_vital_state_id = family_vital_state_id
        self.cancer_type = cancer_type

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'personal_pathological_history_id': self.personal_pathological_history_id,
            'family_id': self.family_id,
            'family_vital_state_id': self.family_vital_state_id,
            'cancer_type': self.cancer_type
        }

        if jsondepth > 0:
            if self.personal_pathological_history:
                json['personal_pathological_history'] = self.personal_pathological_history.json(jsondepth - 1)
            if self.family:
                json['family'] = self.family.json(jsondepth - 1)
            if self.family_vital_state:
                json['family_vital_state'] = self.family_vital_state.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

