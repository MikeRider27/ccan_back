from db import db, BaseModel


class GenderModel(BaseModel):
    __tablename__ = 'gender'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20))

    def __init__(self, id=None, description=None, code=None):
        self.id = id
        self.description = description
        self.code = code

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'code': self.code
        }

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
