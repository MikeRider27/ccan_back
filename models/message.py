from sqlalchemy import func

from db import db, BaseModel
from models.hospital import HospitalModel
from models.patient import PatientModel
from models.user import UserModel


class MessageModel(BaseModel):
    __tablename__ = 'message'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    asunto = db.Column(db.Text, nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_mensaje = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    emisor_id = db.Column(db.BigInteger, db.ForeignKey(UserModel.id), nullable=False)
    isborrado = db.Column(db.Boolean, default=False)
    id_hospital = db.Column(db.INTEGER, nullable=False)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))

    # Relationship
    emisor = db.relationship('UserModel', foreign_keys=[emisor_id], uselist=False)
    destinatarios = db.relationship('DestinatariosModel')
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)

    def __init__(self, id=None, asunto=None, mensaje=None, fecha_mensaje=None, emisor_id=None,
                 isborrado=False, id_hospital=None, patient_id=None):
        self.id = id
        self.asunto = asunto
        self.mensaje = mensaje
        self.fecha_mensaje = fecha_mensaje
        self.emisor_id = emisor_id
        self.isborrado = isborrado
        self.id_hospital = id_hospital
        self.patient_id = patient_id
    def get_nombre_hospital(self):
        if self.id_hospital:
            entidad = HospitalModel.query.get(self.id_hospital)
        else:
            entidad = None

        return entidad.description if entidad else None

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'asunto': self.asunto,
            'mensaje': self.mensaje,
            'fecha_mensaje': self.fecha_mensaje,
            'emisor_id': self.emisor_id,
            'isborrado': self.isborrado,
            'id_hospital': self.id_hospital,
            'nombre_hospital': self.get_nombre_hospital(),
            'patient_id': self.patient_id
        }
        if jsondepth > 0:
            if self.emisor:
                json['emisor'] = self.emisor.json(jsondepth - 1) if self.emisor else None
                json['destinatarios'] = [destinatario.json(jsondepth - 1) for destinatario in self.destinatarios] if self.destinatarios else []
                json['patient'] = self.patient.json(jsondepth - 1) if self.patient else None
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
