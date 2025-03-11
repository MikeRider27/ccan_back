from db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID

from models.treatment_request_scheme import TreatmentRequestSchemeModel


class TreatmentRequestModel(BaseModel):
    __tablename__ = "treatment_request"

    uuid = db.Column(UUID(as_uuid=True), unique=True, default=db.text("uuid_generate_v4()"))
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospital.id'), nullable=False)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patient.id'), nullable=False)
    protocol_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    specialty_id = db.Column(db.BigInteger, db.ForeignKey('specialty.id'))
    diagnosis_id = db.Column(db.BigInteger, db.ForeignKey('diagnosis.id'))
    topography_id = db.Column(db.BigInteger, db.ForeignKey('cie_o_topography.id'))
    morphology_id = db.Column(db.BigInteger, db.ForeignKey('cie_o_morphology.id'))
    stage_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    criteria_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'))
    date = db.Column(db.TIMESTAMP(timezone=True))
    is_urgent = db.Column(db.Boolean)
    status = db.Column(db.SmallInteger, default=1)
    comment = db.Column(db.Text)
    patient_weight = db.Column(db.Numeric(5, 2))
    patient_height = db.Column(db.Numeric(5, 2))
    body_surface_area = db.Column(db.Numeric(5, 2))
    created_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    edited_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    edited_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())



    # TODO: HAY NUEVAS COLUMNAS QUE OLGA CARGO, TENGO QUE AGREGAR ACA, PERO QUIERO TERMINAR PRIMERO LA LOGICA



    # Relationships
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False, lazy="selectin")
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False, lazy="selectin")
    protocol = db.relationship('ParameterModel', foreign_keys=[protocol_id], uselist=False, lazy="selectin")
    specialty = db.relationship('SpecialtyModel', foreign_keys=[specialty_id], uselist=False, lazy="selectin")
    diagnosis = db.relationship('DiagnosisModel', foreign_keys=[diagnosis_id], uselist=False, lazy="selectin")
    topography = db.relationship('CieOTopographyModel', foreign_keys=[topography_id], uselist=False, lazy="selectin")
    morphology = db.relationship('CieOMorphologyModel', foreign_keys=[morphology_id], uselist=False, lazy="selectin")
    stage = db.relationship('ParameterModel', foreign_keys=[stage_id], uselist=False, lazy="selectin")
    criteria = db.relationship('ParameterModel', foreign_keys=[criteria_id], uselist=False, lazy="selectin")
    created_user = db.relationship('UserModel', foreign_keys=[created_user_id], uselist=False, lazy="selectin")
    edited_user = db.relationship('UserModel', foreign_keys=[edited_user_id], uselist=False, lazy="selectin")

    @classmethod
    def query_find_all(cls, hospital_id=None):
        query = cls.query
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)

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

    def json(self, jsondepth=0):
        treatment_scheme = TreatmentRequestSchemeModel.get_current_for_request(self.id)

        data = {
            "uuid": str(self.uuid),
            "hospital_id": self.hospital_id,
            "patient_id": self.patient_id,
            "protocol_id": self.protocol_id,
            "specialty_id": self.specialty_id,
            "diagnosis_id": self.diagnosis_id,
            "topography_id": self.topography_id,
            "morphology_id": self.morphology_id,
            "stage_id": self.stage_id,
            "criteria_id": self.criteria_id,
            "date": self.date,
            "is_urgent": self.is_urgent,
            "status": self.status,
            "comment": self.comment,
            "patient_weight": self.patient_weight,
            "patient_height": self.patient_height,
            "body_surface_area": self.body_surface_area,
            "treatment_scheme": treatment_scheme.json(jsondepth) if treatment_scheme else None
        }
        if jsondepth > 0:
            next_depth = jsondepth - 1
            data["patient"] = self.patient.json() if self.patient_id else None # "0" depth because of too much (unnecessary) data
            data["protocol"] = self.protocol.json(next_depth) if self.protocol_id else None
            data["specialty"] = self.specialty.json(next_depth) if self.specialty_id else None
            data["diagnosis"] = self.diagnosis.json() if self.diagnosis_id else None # "0" depth because of too much (unnecessary) data
            data["topography"] = self.topography.json(next_depth) if self.topography_id else None
            data["morphology"] = self.morphology.json(next_depth) if self.morphology_id else None
            data["stage"] = self.stage.json(next_depth) if self.stage_id else None
            data["criteria"] = self.criteria.json(next_depth) if self.criteria_id else None

        return data
