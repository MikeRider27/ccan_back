import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.committee import CommitteeModel
from models.doctor import DoctorModel


class MedicalCommitteeModel(BaseModel):
    __tablename__ = 'medical_committee'

    id = db.Column(db.BigInteger, primary_key=True)
    committee_id = db.Column(db.BigInteger, db.ForeignKey(CommitteeModel.id))
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))

    committee = db.relationship('CommitteeModel', foreign_keys=[committee_id], uselist=False)
    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)

    def __init__(self, id, committee_id, doctor_id):
        self.id = id
        self.committee_id = committee_id
        self.doctor_id = doctor_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'committee_id': self.committee_id,
            'doctor_id': self.doctor_id
        }

        if jsondepth > 0:
            if self.committee:
                json['committee'] = self.committee.json(jsondepth - 1)
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

