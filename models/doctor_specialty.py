import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.doctor import DoctorModel
from models.specialty import SpecialtyModel


class DoctorSpecialtyModel(BaseModel):
    __tablename__ = 'doctor_specialty'

    id = db.Column(db.BigInteger, primary_key=True)
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    specialty_id = db.Column(db.BigInteger, db.ForeignKey(SpecialtyModel.id))

    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)
    specialty = db.relationship('SpecialtyModel', foreign_keys=[specialty_id], uselist=False)

    def __init__(self, id=None, doctor_id=None, specialty_id=None):
        self.id = id
        self.doctor_id = doctor_id
        self.specialty_id = specialty_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'specialty_id': self.specialty_id
        }

        if jsondepth > 0:
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
            if self.specialty:
                json['specialty'] = self.specialty.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
