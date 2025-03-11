import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.radiotherapy import RadiotherapyModel
from models.treatment_plan import TreatmentPlanModel


class RadiotherapyTreatmentPlanModel(BaseModel):
    __tablename__ = 'radiotherapy_treatment_plan'

    id = db.Column(db.BigInteger, primary_key=True)
    radiotherapy_id = db.Column(db.BigInteger, db.ForeignKey(RadiotherapyModel.id))
    treatment_plan_id = db.Column(db.BigInteger, db.ForeignKey(TreatmentPlanModel.id))
    num_session = db.Column(db.Integer)

    radiotherapy = db.relationship('RadiotherapyModel', foreign_keys=[radiotherapy_id], uselist=False)
    treatment_plan = db.relationship('TreatmentPlanModel', foreign_keys=[treatment_plan_id], uselist=False)

    def __init__(self, id=None, radiotherapy_id=None, treatment_plan_id=None, num_session=None):
        self.id = id
        self.radiotherapy_id = radiotherapy_id
        self.treatment_plan_id = treatment_plan_id
        self.num_session = num_session

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'radiotherapy_id': self.radiotherapy_id,
            'treatment_plan_id': self.treatment_plan_id,
            'num_session': self.num_session
        }

        if jsondepth > 0:
            if self.radiotherapy:
                json['radiotherapy'] = self.radiotherapy.json(jsondepth - 1)
            if self.treatment_plan:
                json['treatment_plan'] = self.treatment_plan.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

