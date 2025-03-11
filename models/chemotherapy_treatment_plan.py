from db import db, BaseModel
from models.chemotherapy import ChemotherapyModel
from models.treatment_plan import TreatmentPlanModel


class ChemotherapyTreatmentPlanModel(BaseModel):
    __tablename__ = 'chemotherapy_treatment_plan'

    id = db.Column(db.BigInteger, primary_key=True)
    chemotherapy_id = db.Column(db.BigInteger, db.ForeignKey(ChemotherapyModel.id))
    treatment_plan_id = db.Column(db.BigInteger, db.ForeignKey(TreatmentPlanModel.id))
    num_session = db.Column(db.Integer)

    chemotherapy = db.relationship('ChemotherapyModel', foreign_keys=[chemotherapy_id], uselist=False)
    treatment_plan = db.relationship('TreatmentPlanModel', foreign_keys=[treatment_plan_id], uselist=False)

    def __init__(self, id=None, chemotherapy_id=None, treatment_plan_id=None, num_session=None):
        self.id = id
        self.chemotherapy_id = chemotherapy_id
        self.treatment_plan_id = treatment_plan_id
        self.num_session = num_session

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'chemotherapy_id': self.chemotherapy_id,
            'treatment_plan_id': self.treatment_plan_id,
            'num_session': self.num_session
        }

        if jsondepth > 0:
            if self.chemotherapy:
                json['chemotherapy'] = self.chemotherapy.json(jsondepth - 1)
            if self.treatment_plan:
                json['treatment_plan'] = self.treatment_plan.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

