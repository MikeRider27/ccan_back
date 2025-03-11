import datetime

from db import db, BaseModel


class MedicineModel(BaseModel):
    __tablename__ = 'medicine'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(100))
    concentration = db.Column(db.String())
    pharmaceutical_form = db.Column(db.String())
    via_admin = db.Column(db.String(100))
    presentation = db.Column(db.String(100))
    code_dgc = db.Column(db.String(100))
    state = db.Column(db.String(1))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    stock_control = db.Column(db.Boolean)
    generic_name = db.Column(db.String(200))

    def __init__(self, id, description, code, concentration, pharmaceutical_form, via_admin, presentation, code_dgc,
                 state, date_create=None, user_create=None, date_modify=None, user_modify=None, stock_control=False,
                 generic_name=None):
        self.id = id
        self.description = description
        self.code = code
        self.concentration = concentration
        self.pharmaceutical_form = pharmaceutical_form
        self.via_admin = via_admin
        self.presentation = presentation
        self.code_dgc = code_dgc
        self.state = state
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.stock_control = stock_control
        self.generic_name = generic_name

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'description': self.description,
            'code': self.code,
            'concentration': self.concentration,
            'pharmaceutical_form': self.pharmaceutical_form,
            'via_admin': self.via_admin,
            'presentation': self.presentation,
            'code_dgc': self.code_dgc,
            'state': self.state,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'stock_control': self.stock_control,
            'generic_name': self.generic_name,
        }

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

