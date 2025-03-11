import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.evaluation import EvaluationModel
from models.user import UserModel


class EvaluatorsModel(BaseModel):
    __tablename__ = 'evaluators'

    id = db.Column(db.BigInteger, primary_key=True)
    evaluation_id = db.Column(db.BigInteger, db.ForeignKey(EvaluationModel.id))
    evaluator_id = db.Column(db.BigInteger, db.ForeignKey(UserModel.id))

    evaluation = db.relationship('EvaluationModel', foreign_keys=[evaluation_id], uselist=False)
    evaluator = db.relationship('UserModel', foreign_keys=[evaluator_id], uselist=False)

    def __init__(self, id=None, evaluation_id=None, evaluator_id=None):
        self.id = id
        self.evaluation_id = evaluation_id
        self.evaluator_id = evaluator_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'evaluation_id': self.evaluation_id,
            'evaluator_id': self.evaluator_id,
        }

        if jsondepth > 0:
            if self.evaluation:
                json['evaluation'] = self.evaluation.json(jsondepth - 1)
            if self.evaluator:
                json['evaluator'] = self.evaluator.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

