from db import db, BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import UniqueConstraint


class ProductModel(BaseModel):
    __tablename__ = "product"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, default=db.text("uuid_generate_v4()"))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospital.id'), nullable=False)
    medicine_id = db.Column(db.BigInteger, db.ForeignKey('medicine.id'), nullable=True)
    drug_id = db.Column(db.BigInteger, db.ForeignKey('drug.id'), nullable=True)
    code = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    concentration = db.Column(db.Numeric(10, 2), nullable=True)
    concentration_unit_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'), nullable=True)
    quantity = db.Column(db.Numeric(10, 2), nullable=True)
    quantity_unit_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'), nullable=True)
    type_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'), nullable=True)
    status = db.Column(db.SmallInteger, nullable=True, default=1)
    premedication = db.Column(db.Text, nullable=True)
    medication = db.Column(db.Text, nullable=True)
    postmedication = db.Column(db.Text, nullable=True)
    dose_limit = db.Column(db.Numeric(10, 2), nullable=True, default=0)
    dose_unit_id = db.Column(db.BigInteger, db.ForeignKey('parameter.id'), nullable=True)
    contraindications = db.Column(db.Text, nullable=True)
    created_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    edited_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.timestamptz_now())
    edited_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.timestamptz_now(),
                          onupdate=db.func.now())

    __table_args__ = (
        UniqueConstraint('hospital_id', 'code', name='uq_hospital_id_code'),
    )

    # Relationships
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False, lazy="selectin")
    medicine = db.relationship('MedicineModel', foreign_keys=[medicine_id], uselist=False, lazy="selectin")
    drug = db.relationship('DrugModel', foreign_keys=[drug_id], uselist=False, lazy="selectin")
    concentration_unit = db.relationship('ParameterModel', foreign_keys=[concentration_unit_id], uselist=False, lazy="selectin")
    quantity_unit = db.relationship('ParameterModel', foreign_keys=[quantity_unit_id], uselist=False, lazy="selectin")
    type = db.relationship('ParameterModel', foreign_keys=[type_id], uselist=False, lazy="selectin")
    dose_unit = db.relationship('ParameterModel', foreign_keys=[dose_unit_id], uselist=False, lazy="selectin")
    created_user = db.relationship('UserModel', foreign_keys=[created_user_id], uselist=False, lazy="selectin")
    edited_user = db.relationship('UserModel', foreign_keys=[edited_user_id], uselist=False, lazy="selectin")

    @classmethod
    def query_find_all(cls, hospital_id=None):
        query = cls.query
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)

        return query


    @classmethod
    def exists_by_hospital_and_code(cls, hospital_id: int, code: str) -> bool:
        return cls.query.filter_by(hospital_id=hospital_id, code=code).first() is not None


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
        data = {
            "uuid": str(self.uuid),
            "medicine_id": self.medicine_id,
            "drug_id": self.drug_id,
            "code": self.code,
            "description": self.description,
            "concentration": self.concentration,
            "concentration_unit_id": self.concentration_unit_id,
            "quantity": self.quantity,
            "quantity_unit_id": self.quantity_unit_id,
            "type_id": self.type_id,
            "status": self.status,
            "medication": self.medication,
            "premedication": self.premedication,
            "postmedication": self.postmedication,
            "dose_limit": self.dose_limit,
            "dose_unit_id": self.dose_unit_id,
            "contraindications": self.contraindications,
            # "created_at": self.created_at.isoformat() if self.created_at else None,
            # "edited_at": self.edited_at.isoformat() if self.edited_at else None,
        }

        if jsondepth > 0:
            next_depth = jsondepth - 1
            data["hospital"] = self.hospital.json(next_depth) if self.hospital_id else None
            data["medicine"] = self.medicine.json(next_depth) if self.medicine_id else None
            data["drug"] = self.drug.json(next_depth) if self.drug_id else None
            data["concentration_unit"] = self.concentration_unit.json(next_depth) if self.concentration_unit_id else None
            data["quantity_unit"] = self.quantity_unit.json(next_depth) if self.quantity_unit_id else None
            data["type"] = self.type.json(next_depth) if self.type_id else None
            data["dose_unit"] = self.dose_unit.json(next_depth) if self.dose_unit_id else None

        return data
