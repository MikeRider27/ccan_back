import datetime
from enum import Enum

from db import db, BaseModel
from models.deposit_stock import DepositStockModel
from models.parameter import ParameterModel
from models.patient import OriginsCode


class EventCode(Enum):
    ADD_BY_LOTE = 'ADD_BY_LOTE'
    REMOVE_BY_LOTE = 'REMOVE_BY_LOTE'
    AJUST_STOCK = 'AJUST_STOCK'
    DEPOSIT_MOV = 'DEPOSIT_MOV'
    DISPENSE_PAT = 'DISPENSE_PAT'
    DISPENSE_REVERT = 'DISPENSE_REVERT'
    ADD_BY_ENTRY = 'ADD_BY_ENTRY'
    REMOVE_BY_ENTRY = 'REMOVE_BY_ENTRY'
    ADD_BY_MEDICINE_TREATMENT_FOLLOW_UP = 'ADD_BY_M_T_F_U'
    REMOVE_BY_MEDICINE_TREATMENT_FOLLOW_UP = 'REMOVE_BY_M_T_F_U'
    SYNC_SICIAP = 'SYNC_SICIAP'


class HistoryModel(BaseModel):
    __tablename__ = 'history'
    __table_args__ = {"schema": "inventory"}

    id = db.Column(db.BigInteger, primary_key=True)
    orig_deposit_stock_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id), nullable=False)
    dest_deposit_stock_id = db.Column(db.BigInteger, db.ForeignKey(DepositStockModel.id))
    quantity = db.Column(db.Float, nullable=False)
    event_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id), nullable=False)
    description = db.Column(db.String(500))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    origin = db.Column(db.String(30), nullable=False, default=OriginsCode.CCAN_CITY_SOFT.value)
    date = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now)
    observation = db.Column(db.Text)
    balance = db.Column(db.Float, nullable=False)
    original_quantity = db.Column(db.Float, nullable=False)
    num_lot = db.Column(db.String(50))

    orig_deposit_stock = db.relationship('DepositStockModel', foreign_keys=[orig_deposit_stock_id], uselist=False)
    dest_deposit_stock = db.relationship('DepositStockModel', foreign_keys=[dest_deposit_stock_id], uselist=False)
    event = db.relationship('ParameterModel', foreign_keys=[event_id], uselist=False)

    def __init__(self, id=None, orig_deposit_stock_id=None, dest_deposit_stock_id=None, quantity=None, event_id=None,
                 description=None, date_create=None, user_create=None, origin=None, date=None, observation=None,
                 balance=None, original_quantity=None, num_lot=None):
        self.id = id
        self.orig_deposit_stock_id = orig_deposit_stock_id
        self.dest_deposit_stock_id = dest_deposit_stock_id
        self.quantity = quantity
        self.event_id = event_id
        self.description = description
        self.date_create = date_create
        self.user_create = user_create
        self.origin = origin
        self.date = date
        self.observation = observation
        self.balance = balance
        self.original_quantity = original_quantity
        self.num_lot = num_lot

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'quantity': self.quantity,
            'event_id': self.event_id,
            'description': self.description,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'origin': self.origin,
            'date': self.date.strftime("%d/%m/%Y %H:%M:%S") if self.date else None,
            'observation': self.observation,
            'balance': self.balance,
            'original_quantity': self.original_quantity,
            'num_lot': self.num_lot,
        }

        if jsondepth > 0:
            if self.orig_deposit_stock:
                json['orig_deposit_stock'] = self.orig_deposit_stock.json(jsondepth - 1)
            if self.dest_deposit_stock:
                json['dest_deposit_stock'] = self.dest_deposit_stock.json(jsondepth - 1)
            if self.event:
                json['event'] = self.event.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_event(cls, event: EventCode):
        parameter = ParameterModel.query.filter_by(code=event.value).first()
        if parameter:
            return parameter.id

        return None
