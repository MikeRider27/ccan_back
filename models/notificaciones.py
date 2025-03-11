from db import db, BaseModel
from models.message import MessageModel
from models.user import UserModel

class NotificacionesModel(BaseModel):
    __tablename__ = 'notificaciones'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(UserModel.id), nullable=False)
    message_id = db.Column(db.BigInteger,db.ForeignKey(MessageModel.id), nullable=False)
    leida = db.Column(db.Boolean, default=False)

    # Relationship
    user = db.relationship('UserModel', foreign_keys=[user_id], uselist=False)
    mensaje = db.relationship('MessageModel', foreign_keys=[message_id], uselist=False)

    def __init__(self, id=None, user_id=None, message_id=None, leida=False):
        self.id = id
        self.user_id = user_id
        self.message_id = message_id
        self.leida = leida

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'user_id': self.user_id,
            'message_id': self.message_id,
            'leida': self.leida
        }
        if jsondepth > 0:
            if self.user:
                json['user'] = self.user.json(jsondepth - 1)
            if self.mensaje:
                json['mensaje'] = self.mensaje.json(jsondepth - 1)

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
