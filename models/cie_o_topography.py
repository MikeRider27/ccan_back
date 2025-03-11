from db import db, BaseModel
from models.gender import GenderModel


class CieOTopographyModel(BaseModel):
    __tablename__ = 'cie_o_topography'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    code = db.Column(db.String(100))
    description_es = db.Column(db.String(100))
    description_en = db.Column(db.String(100))
    gender_id = db.Column(db.BigInteger)

    def __init__(self, id, code, description_es, description_en, gender_id):
        self.id = id
        self.code = code
        self.description_es = description_es
        self.description_en = description_en
        self.gender_id = gender_id

    def get_gender(self):
        if self.gender_id:
            gender = GenderModel.query.get(self.gender_id)
        else:
            gender = None

        return gender.description if gender else None
    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'code': self.code,
            'description_es': self.description_es,
            'description_en': self.description_en,
            'gender_id': self.gender_id,
            'gender': self.get_gender(),
        }
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

