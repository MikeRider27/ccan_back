import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.treatment_follow_up import TreatmentFollowUpModel
from models.treatment_plan import TreatmentPlanModel


class FollowUpTreatmentPlanModel(BaseModel):
    __tablename__ = 'follow_up_treatment_plan'

    id = db.Column(db.BigInteger, primary_key=True)
    follow_up_id = db.Column(db.BigInteger, db.ForeignKey(TreatmentFollowUpModel.id))
    treatment_plan_id = db.Column(db.BigInteger, db.ForeignKey(TreatmentPlanModel.id))

    treatment_follow_up = db.relationship('TreatmentFollowUpModel', foreign_keys=[follow_up_id], uselist=False)
    treatment_plan = db.relationship('TreatmentPlanModel', foreign_keys=[treatment_plan_id], uselist=False)

    def __init__(self, id=None, follow_up_id=None, treatment_plan_id=None):
        self.id = id
        self.follow_up_id = follow_up_id
        self.treatment_plan_id = treatment_plan_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'follow_up_id': self.follow_up_id,
            'treatment_plan_id': self.treatment_plan_id,
        }

        if jsondepth > 0:
            if self.treatment_follow_up:
                json['treatment_follow_up'] = self.treatment_follow_up.json(jsondepth - 1)
            if self.treatment_plan:
                json['treatment_plan'] = self.treatment_plan.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

