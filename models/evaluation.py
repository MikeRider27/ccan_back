import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.patient import PatientModel


class EvaluationModel(BaseModel):
    __tablename__ = 'evaluation'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    observation = db.Column(db.String)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    evaluation_state = db.Column(db.String(10))

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    evaluator_list = db.relationship('EvaluatorsModel', cascade="all, delete-orphan")

    def __init__(self, id=None, patient_id=None, date_start=None, date_end=None, observation=None, date_create=None,
                 user_create=None, date_modify=None, user_modify=None, evaluation_state=None):
        self.id = id
        self.patient_id = patient_id
        self.date_start = date_start
        self.date_end = date_end
        self.observation = observation
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.evaluation_state = evaluation_state

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'date_start': self.date_start.strftime("%d/%m/%Y") if self.date_start else None,
            'date_end': self.date_end.strftime("%d/%m/%Y") if self.date_end else None,
            'observation': self.observation,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'evaluation_state': self.evaluation_state
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            json['evaluator_list'] = []
            if self.evaluator_list:
                for evaluator in self.evaluator_list:
                    json['evaluator_list'].append(evaluator.json(jsondepth - 1))
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

