import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.surgery import SurgeryModel
from models.doctor import DoctorModel


class MedicalTeamModel(BaseModel):
    __tablename__ = 'medical_team'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    surgery_id = db.Column(db.BigInteger, db.ForeignKey(SurgeryModel.id))
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    rol = db.Column(db.String(100))
    nurse = db.Column(db.String)
    anesthetist = db.Column(db.String)
    surgical_instrumentator = db.Column(db.String)
    technical = db.Column(db.String)

    surgery = db.relationship('SurgeryModel', foreign_keys=[surgery_id], uselist=False)
    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)

    def __init__(self, id=None, surgery_id=None, doctor_id=None, rol=None, nurse=None, anesthetist=None, surgical_instrumentator=None, technical=None):
        self.id = id
        self.surgery_id = surgery_id
        self.doctor_id = doctor_id
        self.rol = rol
        self.nurse = nurse
        self.anesthetist = anesthetist
        self.surgical_instrumentator = surgical_instrumentator
        self.technical = technical

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'surgery_id': self.surgery_id,
            'doctor_id': self.doctor_id,
            'rol': self.rol,
            'nurse': self.nurse,
            'anesthetist': self.anesthetist,
            'surgical_instrumentator': self.surgical_instrumentator,
            'technical': self.technical
        }

        if jsondepth > 0:
            if self.surgery:
                json['surgery'] = self.surgery.json(jsondepth - 1)
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

