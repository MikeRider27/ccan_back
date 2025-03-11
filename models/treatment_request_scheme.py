from db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID


class TreatmentRequestSchemeModel(BaseModel):
    __tablename__ = "treatment_request_scheme"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, default=db.text("uuid_generate_v4()"))
    treatment_request_id = db.Column(db.BigInteger, db.ForeignKey('treatment_request.id'), nullable=False)
    treatment_scheme_id = db.Column(db.BigInteger, db.ForeignKey('treatment_scheme.id'), nullable=False)
    base_treatment_scheme_id = db.Column(db.BigInteger, db.ForeignKey('treatment_scheme.id'))
    previous_treatment_scheme_id = db.Column(db.BigInteger, db.ForeignKey('treatment_scheme.id'))

    # Relationships
    # treatment_request = db.relationship('TreatmentRequestModel', foreign_keys=[treatment_request_id], uselist=False,
    #                                     lazy="selectin")
    treatment_scheme = db.relationship('TreatmentSchemeModel', foreign_keys=[treatment_scheme_id], uselist=False,
                                       lazy="selectin")
    base_treatment_scheme = db.relationship('TreatmentSchemeModel', foreign_keys=[base_treatment_scheme_id],
                                            uselist=False, lazy="selectin")
    # previous_treatment_scheme = db.relationship('TreatmentSchemeModel', foreign_keys=[previous_treatment_scheme_id],
    #                                             uselist=False, lazy="selectin")

    @classmethod
    def query_find_all(cls):
        query = cls.query
        return query

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def get_current_for_request(cls, request_id):
        return (
            cls.query
            .filter_by(treatment_request_id=request_id)
            .order_by(TreatmentRequestSchemeModel.id.desc())
            .limit(1)
            .first()
        )

    def json(self, jsondepth=0):
        next_depth = jsondepth - 1
        data = self.treatment_scheme.json(next_depth) if self.treatment_scheme else {}

        data["uuid"] = str(self.uuid)
        data["treatment_request_id"] = self.treatment_request_id
        data["treatment_scheme_id"] = self.treatment_scheme_id
        data["base_treatment_scheme_id"] = self.base_treatment_scheme_id
        data["previous_treatment_scheme_id"] = self.previous_treatment_scheme_id

        if jsondepth > 0:
        #     data["treatment_request"] = self.treatment_request.json(next_depth) if self.treatment_request_id else None
        #     data["treatment_scheme"] = self.treatment_scheme.json(next_depth) if self.treatment_scheme_id else None
            data["base_treatment_scheme"] = self.base_treatment_scheme.json(next_depth) if self.base_treatment_scheme_id else None
        #     data["previous_treatment_scheme"] = self.previous_treatment_scheme.json(
        #         next_depth) if self.previous_treatment_scheme_id else None

        return data
