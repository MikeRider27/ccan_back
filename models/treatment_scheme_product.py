from db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID

from models.treatment_scheme import TreatmentRequestTypeEnum


class TreatmentSchemeProductModel(BaseModel):
    __tablename__ = "treatment_scheme_product"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), default=db.text("uuid_generate_v4()"), unique=True, nullable=False)
    treatment_scheme_id = db.Column(db.BigInteger, db.ForeignKey('treatment_scheme.id'), nullable=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False)
    administration_route_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    calculation_type_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    frequency_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    note = db.Column(db.Text)
    adjustable = db.Column(db.Boolean)
    adjust_comment = db.Column(db.Boolean)
    status = db.Column(db.SmallInteger, default=1)
    index = db.Column(db.SmallInteger)
    loading_dose = db.Column(db.Numeric(10, 2))
    session_dose = db.Column(db.Numeric(10, 2))
    infusion_dose = db.Column(db.Numeric(10, 2))
    created_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    edited_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    edited_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())

    # Relationships
    treatment_scheme = db.relationship('TreatmentSchemeModel', foreign_keys=[treatment_scheme_id],
                                       backref=db.backref('scheme_products', lazy='selectin'), uselist=False, lazy='selectin')
    product = db.relationship('ProductModel', foreign_keys=[product_id], uselist=False, lazy='selectin')
    administration_route = db.relationship('ParameterModel', foreign_keys=[administration_route_id], uselist=False,
                                           lazy='selectin')
    calculation_type = db.relationship('ParameterModel', foreign_keys=[calculation_type_id], uselist=False,
                                       lazy='selectin')
    frequency = db.relationship('ParameterModel', foreign_keys=[frequency_id], uselist=False, lazy='selectin')
    created_user = db.relationship('UserModel', foreign_keys=[created_user_id], uselist=False, lazy='selectin')
    edited_user = db.relationship('UserModel', foreign_keys=[edited_user_id], uselist=False, lazy='selectin')

    # Methods
    @classmethod
    def query_find_all(cls):
        query = cls.query.filter_by(status=1)
        return query

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_uuid(cls, uuid):
        query = cls.query.filter_by(uuid=uuid)
        return query.first()

    def json(self, jsondepth=0):
        data = {
            "uuid": str(self.uuid),
            "treatment_scheme_id": self.treatment_scheme_id,
            "product_id": self.product_id,
            "administration_route_id": self.administration_route_id,
            "calculation_type_id": self.calculation_type_id,
            "frequency_id": self.frequency_id,
            "note": self.note,
            "adjustable": self.adjustable,
            "status": self.status,
            "loading_dose": self.loading_dose,
            "session_dose": self.session_dose,
            "infusion_dose": self.infusion_dose,
            "edited_at": self.edited_at.isoformat() if self.edited_at else None
        }

        if self.treatment_scheme.type == TreatmentRequestTypeEnum.TREATMENT_REQUEST_SCHEMA.value:
            data["adjust_comment"] = self.adjust_comment
            data["index"] = self.index

        if jsondepth > 0:
            next_depth = jsondepth - 1
            # data["treatment_scheme"] = self.treatment_scheme.json(next_depth) if self.treatment_scheme_id else None
            data["product"] = self.product.json(next_depth) if self.product_id else None
            data["administration_route"] = self.administration_route.json(
                next_depth) if self.administration_route_id else None
            data["calculation_type"] = self.calculation_type.json(next_depth) if self.calculation_type_id else None
            data["frequency"] = self.frequency.json(next_depth) if self.frequency_id else None

        return data
