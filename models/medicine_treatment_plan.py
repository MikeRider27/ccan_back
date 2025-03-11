from db import db, BaseModel
from models.medicine import MedicineModel
from models.treatment_plan import TreatmentPlanModel


class MedicineTreatmentPlanModel(BaseModel):
    __tablename__ = 'medicine_treatment_plan'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    medicine_id = db.Column(db.BigInteger, db.ForeignKey(MedicineModel.id))
    treatment_plan_id = db.Column(db.BigInteger, db.ForeignKey(TreatmentPlanModel.id))
    quantity = db.Column(db.Numeric)
    observation = db.Column(db.String)
    dose = db.Column(db.Numeric)
    presentation = db.Column(db.String)
    concentration = db.Column(db.String)

    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False)
    treatment_plan = db.relationship('TreatmentPlanModel', foreign_keys=[treatment_plan_id], uselist=False)

    def __init__(self, id, medicine_id, treatment_plan_id, quantity, observation, dose, presentation=None, concentration=None):
        self.id = id
        self.medicine_id = medicine_id
        self.treatment_plan_id = treatment_plan_id
        self.quantity = quantity
        self.observation = observation
        self.dose = dose
        self.presentation = presentation
        self.concentration = concentration

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'treatment_plan_id': self.treatment_plan_id,
            'quantity': self.quantity,
            'observation': self.observation,
            'dose': self.dose,
            'presentation': self.presentation,
            'concentration': self.concentration,
        }

        if jsondepth > 0:
            if self.medicine:
                json['medicine'] = self.medicine.json(jsondepth - 1)
            if self.treatment_plan:
                json['treatment_plan'] = self.treatment_plan.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

