from db import db, BaseModel
from models.parameter_translation import ParameterTranslationModel # needed for the 'translations' attribute (backref from ParameterTranslationModel)


class ParameterModel(BaseModel):
    __tablename__ = 'parameter'

    id = db.Column(db.BigInteger, primary_key=True)
    domain = db.Column(db.String(100))
    value = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    code = db.Column(db.String(20))

    def __init__(self, id=None, domain=None, value=None, active=None, code=None):
        self.id = id
        self.domain = domain
        self.value = value
        self.active = active
        self.code = code

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'domain': self.domain,
            'value': self.value,
            'active': self.active,
            'code': self.code,
            'translations': {translation.language_code: translation.json() for translation in self.translations}
        }

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_domain(cls, domain):
        return cls.query.filter_by(domain=domain).first()
