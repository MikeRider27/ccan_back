from db import db, BaseModel
from models.cie_o_topography import CieOTopographyModel


class CieOTumorLocationModel(BaseModel):
    __tablename__ = 'cie_o_tumor_location'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    code = db.Column(db.String(100))
    description_es = db.Column(db.String(100))
    description_en = db.Column(db.String(100))
    cie_o_topography_id = db.Column(db.BigInteger)
    def __init__(self, id, code, description_es, description_en, cie_o_topography_id):
        self.id = id
        self.code = code
        self.description_es = description_es
        self.description_en = description_en
        self.cie_o_topography_id = cie_o_topography_id

    def get_cie_o_topography(self):
        if self.cie_o_topography_id:
            cieo = CieOTopographyModel.query.get(self.cie_o_topography_id)
        else:
            cieo = None

        return cieo.description_es if cieo else None
    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'code': self.code,
            'description_es': self.description_es,
            'description_en': self.description_en,
            'cie_o_topography_id': self.cie_o_topography_id,
            'cie_o_topography': self.get_cie_o_topography()
        }
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

