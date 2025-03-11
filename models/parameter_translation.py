from db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID


class ParameterTranslationModel(BaseModel):
    __tablename__ = "parameter_translation"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=db.func.uuid_generate_v4())
    parameter_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id', ondelete='CASCADE'), nullable=False)
    language_code = db.Column(db.String(10), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.timestamptz_now())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.timestamptz_now(), onupdate=db.func.timestamptz_now())

    parameter = db.relationship('ParameterModel', foreign_keys=[parameter_id],
                                       backref=db.backref("translations", lazy="selectin"), uselist=False, lazy='selectin')


    @classmethod
    def query_find_all(cls):
        return cls.query

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def json(self, jsondepth=0):
        return {
            'uuid': str(self.uuid),
            'parameter_id': self.parameter_id,
            'language_code': self.language_code,
            'value': self.value,
            'description': self.description
        }
