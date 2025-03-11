from db import db, BaseModel
from enum import Enum
from flask import request
from sqlalchemy.dialects.postgresql import UUID


class TreatmentRequestTypeEnum(Enum):
    BASE_SCHEMA = 1
    TREATMENT_REQUEST_SCHEMA = 2


class TreatmentSchemeModel(BaseModel):
    __tablename__ = "treatment_scheme"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, default=db.text("uuid_generate_v4()"))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    periodicity_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    series_count = db.Column(db.SmallInteger)
    pre_medication = db.Column(db.Text)
    medication = db.Column(db.Text)
    post_medication = db.Column(db.Text)
    category_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    notes = db.Column(db.Text)
    administration_time = db.Column(db.SmallInteger)
    preparation_instructions = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=1)
    type = db.Column(db.SmallInteger, default=TreatmentRequestTypeEnum.BASE_SCHEMA.value, nullable=False)
    created_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    edited_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    edited_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())

    # Relationships
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False, lazy="selectin")
    periodicity = db.relationship('ParameterModel', foreign_keys=[periodicity_id], uselist=False, lazy="selectin")
    category = db.relationship('ParameterModel', foreign_keys=[category_id], uselist=False, lazy="selectin")
    created_user = db.relationship('UserModel', foreign_keys=[created_user_id], uselist=False, lazy="selectin")
    edited_user = db.relationship('UserModel', foreign_keys=[edited_user_id], uselist=False, lazy="selectin")

    @classmethod
    def query_find_all(cls, hospital_id=None, type_id=TreatmentRequestTypeEnum.BASE_SCHEMA.value):
        query = cls.query
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)

        if type_id:
            query = query.filter_by(type=type_id)

        return query

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_uuid(cls, uuid, hospital_id=None):
        query = cls.query.filter_by(uuid=uuid)
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)

        return query.first()

    @classmethod
    def get_by_name(cls, name, hospital_id, type_id=TreatmentRequestTypeEnum.BASE_SCHEMA.value):
        return cls.query.filter_by(name=name, hospital_id=hospital_id, type=type_id).first()

    def json(self, jsondepth=0, active_only=False):
        data = {
            "uuid": str(self.uuid),
            "hospital_id": self.hospital_id,
            "name": self.name,
            "description": self.description,
            "periodicity_id": self.periodicity_id,
            "series_count": self.series_count,
            "pre_medication": self.pre_medication,
            "medication": self.medication,
            "post_medication": self.post_medication,
            "category_id": self.category_id,
            "notes": self.notes,
            "administration_time": self.administration_time,
            "preparation_instructions": self.preparation_instructions,
            "status": self.status,
            # "type": self.type,
            # "created_user_id": self.created_user_id,
            # "edited_user_id": self.edited_user_id,
            # "created_at": self.created_at,
            # "edited_at": self.edited_at,
        }
        if jsondepth > 0:
            next_depth = jsondepth - 1
            data["periodicity"] = self.periodicity.json(next_depth) if self.periodicity_id else None
            data["category"] = self.category.json(next_depth) if self.category_id else None
            # data["created_user"] = self.created_user.json(next_depth) if self.created_user else None
            # data["edited_user"] = self.edited_user.json(next_depth) if self.edited_user else None

            default_active_value = 1 if active_only else 0
            if request.args.get('active_only', default_active_value, int) == 1:
                data["scheme_products"] = [
                    _scheme_product.json(next_depth) for _scheme_product in self.scheme_products if
                    _scheme_product.status == 1
                ]
            else:
                data["scheme_products"] = [_scheme_product.json(next_depth) for _scheme_product in self.scheme_products]

        return data
