from db import db, BaseModel
from models.message import MessageModel
from models.parameter import ParameterModel
from models.user import UserModel

class DestinatariosModel(BaseModel):
    __tablename__ = 'destinatarios'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    message_id = db.Column(db.BigInteger,db.ForeignKey(MessageModel.id), nullable=False)
    destinatarios_id = db.Column(db.BigInteger, db.ForeignKey(UserModel.id), nullable=False)
    estado_id = db.Column(db.BigInteger,db.ForeignKey(ParameterModel.id), nullable=False)
    isborrado = db.Column(db.Boolean, default=False)

    # Relationship
    mensajes = db.relationship('MessageModel', foreign_keys=[message_id], uselist=False)
    destinatarios = db.relationship('UserModel', foreign_keys=[destinatarios_id], uselist=False)
    estado = db.relationship('ParameterModel', foreign_keys=[estado_id], uselist=False)

    def __init__(self, id=None, message_id=None, destinatarios_id=None, estado_id=None, isborrado=False):
        self.id = id
        self.message_id = message_id
        self.destinatarios_id = destinatarios_id
        self.estado_id = estado_id,
        self.isborrado = isborrado

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'message_id': self.message_id,
            'destinatarios_id': self.destinatarios_id,
            'estado_id': self.estado_id,
            'isborrado': self.isborrado
        }
        if jsondepth > 0:
            json['mensajes'] = self.mensajes.json(jsondepth - 1) if self.mensajes else None
            json['destinatarios'] = self.destinatarios.json(jsondepth - 1) if self.destinatarios else None
            json['estado'] = self.estado.json(jsondepth - 1) if self.estado else None

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
