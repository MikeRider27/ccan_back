from db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import UniqueConstraint


class DrugModel(BaseModel):
    __tablename__ = "drug"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, default=db.text("uuid_generate_v4()"))
    generic_name = db.Column(db.String(200), nullable=False)
    therapeutic_action = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'), nullable=True)
    status = db.Column(db.SmallInteger, nullable=True, default=1)
    created_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    edited_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    edited_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('generic_name', name='uq_drug_generic_name'),
    )

    category = db.relationship('ParameterModel', foreign_keys=[category_id], uselist=False, lazy="selectin")
    created_user = db.relationship('UserModel', foreign_keys=[created_user_id], uselist=False, lazy="selectin")
    edited_user = db.relationship('UserModel', foreign_keys=[edited_user_id], uselist=False, lazy="selectin")

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
        data = {
            "uuid": str(self.uuid),
            "generic_name": self.generic_name,
            "therapeutic_action": self.therapeutic_action,
            "category_id": self.category_id,
            "status": self.status,
            # "created_at": self.created_at.isoformat() if self.created_at else None,
            # "edited_at": self.edited_at.isoformat() if self.edited_at else None,
        }

        if jsondepth > 0:
            next_depth = jsondepth - 1
            data["category"] = self.category.json(next_depth) if self.category else None

        return data
