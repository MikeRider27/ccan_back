import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy import and_, or_, cast, func

from db import db
from models.deposit import DepositModel
from models.deposit_lot import DepositLotModel
from models.deposit_stock import DepositStockModel
from models.entries import EntriesModel
from models.entries_lot import EntriesLotModel
from models.history import HistoryModel, EventCode
from models.lot import LotModel
from models.manufacturer import ManufacturerModel
from models.medicine import MedicineModel
from models.parameter import ParameterModel
from models.stock import StockModel
from models.supplier import SupplierModel
from security import check
from utils import restrict, paginated_results, restrict_collector
import sqlalchemy


def add_entries_to_stock(entry):
    # TODO: tener en cuenta el estado del medicamento y del stock
    # Se obtiene el stock del medicamento
    stock = StockModel.query.filter_by(medicine_id=entry.medicine_id).first()

    # Se obtiene el deposito stock
    deposito_stock = None
    if stock:
        deposito_stock = DepositStockModel.query.filter_by(deposit_id=entry.deposit_id,
                                                           stock_id=stock.id).first()
        stock.quantity += entry.quantity
        db.session.add(stock)
    else:
        stock_state = ParameterModel.query.filter_by(domain='STOCK_STATE', code='A').first()
        stock = StockModel(id=None, medicine_id=entry.medicine_id, quantity=entry.quantity,
                           state_id=stock_state.id)
        db.session.add(stock)
        db.session.flush()

    # Se actualiza el depósito stock
    if deposito_stock:
        deposito_stock.quantity += entry.quantity
    else:
        deposito_stock = DepositStockModel(id=None, deposit_id=entry.deposit_id,
                                           stock_id=stock.id, quantity=entry.quantity)
    db.session.add(deposito_stock)
    db.session.flush()

    # Obtener el deposit_lot si existe
    deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposito_stock.id, lote_id=entry.lote_id, medicine_id=entry.medicine_id).first()

    # Se actualiza o agrega el deposit_lot
    if deposit_lot:
        deposit_lot.quantity += entry.quantity
    else:
        deposit_lot = DepositLotModel(id=None, deposit_stock_id=deposito_stock.id, lote_id=entry.lote_id,
                                      medicine_id=entry.medicine_id, quantity=entry.quantity)
    db.session.add(deposit_lot)

    num_lot = LotModel.query.filter_by(id=entry.lote_id).first()

    # Se registra en historial
    historial = HistoryModel()
    historial.orig_deposit_stock = deposito_stock
    historial.quantity = entry.quantity
    historial.event_id = HistoryModel.get_event(EventCode.ADD_BY_ENTRY)
    historial.description = f"Add by entry"
    historial.user_create = get_jwt_identity()
    historial.num_lot = num_lot.num_lot
    db.session.add(historial)


def delete_entries_to_stock(entry):
    # Se obtiene el stock del medicamento
    stock = StockModel.query.filter_by(medicine_id=entry.medicine_id).first()

    # Se obtiene el deposito stock
    if stock:
        deposito_stock = DepositStockModel.query.filter_by(deposit_id=entry.deposit_id,
                                                           stock_id=stock.id).first()
        if deposito_stock:
            # Obtener el deposit_lot
            deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposito_stock.id, lote_id=entry.lote_id,
                                                          medicine_id=entry.medicine_id).first()
            final_quantity = deposito_stock.quantity - entry.quantity
            if final_quantity >= 0:
                deposito_stock.quantity = final_quantity
                deposit_lot.quantity = final_quantity
                stock.quantity -= entry.quantity
                db.session.delete(deposit_lot)
                num_lot = LotModel.query.filter_by(id=entry.lote_id).first()

                # Se registra en historial
                historial = HistoryModel()
                historial.orig_deposit_stock = deposito_stock
                historial.quantity = -entry.quantity
                historial.event_id = HistoryModel.get_event(EventCode.REMOVE_BY_ENTRY)
                historial.description = f"Delete Entry"
                historial.user_create = get_jwt_identity()
                historial.num_lot = num_lot.num_lot
                db.session.add(historial)
            else:
                raise Exception(_("ENTRIES_CREATE_0"))
        else:
            raise Exception(_("ENTRIES_DEPOSIT_STOCK_NOT_FOUND"))
    else:
        raise Exception(_("STOCK_NOT_FOUND"))


def update_entries_to_stock(entry_new, entry_old):
    # Actualizar el lote
    if entry_new.lote_id != entry_old.lote_id:
        delete_lot(entry_old)
        add_lot(entry_new)

    # Verificar si ha cambiado la medicina, el deposito o la cantidad
    change = False
    if entry_new.medicine_id != entry_old.medicine_id:
        change = True
    if entry_new.deposit_id != entry_old.deposit_id:
        change = True
    if entry_new.quantity != entry_old.quantity:
        change = True
    if change:
        delete_entries_to_stock(entry_old)
        add_entries_to_stock(entry_new)


def add_lot(entry):
    # Agregar entrada al lote
    lot = LotModel.query.filter_by(id=entry.lote_id).first()
    lot_entries = EntriesLotModel()
    if lot:
        lot_entries.lot_id = lot.id
        lot_entries.entries_id = entry.id
        db.session.add(lot_entries)

    # lot_entries = LotModel.query.filter_by(id=entry.lote_id).first()
    # lot = EntriesLotModel()
    # if lot_entries:
    #     lot.lot_id = lot_entries.id
    #     lot.entries_id = entry.id
    # db.session.add(lot)


def delete_lot(entry):
    lot = LotModel.query.filter_by(id=entry.lote_id).first()
    lot_entries = EntriesLotModel.query.filter_by(lot_id=lot.id, entries_id=entry.id).first()
    db.session.delete(lot_entries)


class Entries(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('deposit_id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('expiration_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('quantity', type=float)
    parser.add_argument('manufacturer_id', type=int)
    parser.add_argument('manufacturing_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('supplier_id', type=int)
    parser.add_argument('storage_conditions', type=str)
    parser.add_argument('observation', type=str)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('origin', type=str)
    parser.add_argument('lote_id', type=int)

    @jwt_required()
    @check('entries_get')
    @swag_from('../swagger/entries/get_entries.yaml')
    def get(self, id):
        entries = EntriesModel.find_by_id(id)
        if entries:
            return entries.json()
        return {'message': _("ENTRIES_NOT_FOUND")}, 404

    @jwt_required()
    @check('entries_update')
    @swag_from('../swagger/entries/put_entries.yaml')
    def put(self, id):
        entry = EntriesModel.find_by_id(id)
        if entry:
            newdata = Entries.parser.parse_args()
            try:
                with db.session.no_autoflush:
                    update_entries_to_stock(newdata, entry)

                    # Se persisiten todos los cambios
                    EntriesModel.from_reqparse(entry, newdata)
                    db.session.add(entry)
                    db.session.commit()
            except Exception as error:
                # Se revierte los cambios
                db.session.rollback()
                msg = _("ENTRIES_UPDATE_ERROR")
                logging.error(msg, exc_info=error)
                return {"message": msg}, 500

            return entry.json()
        return {'message': _("ENTRIES_NOT_FOUND")}, 404

    @jwt_required()
    @check('entries_delete')
    @swag_from('../swagger/entries/delete_entries.yaml')
    def delete(self, id):
        entries = EntriesModel.find_by_id(id)
        if entries:
            delete_lot(entries)
            entries.delete_from_db()

        return {'message': _("ENTRIES_DELETED")}


class EntriesList(Resource):

    @jwt_required()
    @check('entries_list')
    @swag_from('../swagger/entries/list_entries.yaml')
    def get(self):
        query = EntriesModel.query
        return paginated_results(query)

    @jwt_required()
    @check('entries_insert')
    @swag_from('../swagger/entries/post_entries.yaml')
    def post(self):
        data = Entries.parser.parse_args()

        id = data.get('id')

        if id is not None and EntriesModel.find_by_id(id):
            return {'message': _("ENTRIES_DUPLICATED").format(id)}, 400

        try:
            # Se convierte a transaccional
            with db.session.no_autoflush:
                entry = EntriesModel(**data)
                add_entries_to_stock(entry)

                # Se persisiten todos los cambios
                db.session.add(entry)
                db.session.flush()
                add_lot(entry)
                db.session.commit()
        except Exception as e:
            # Se revierte los cambios
            db.session.rollback()
            msg = _("ENTRIES_CREATE_ERROR")
            logging.error(msg, exc_info=e)
            return {"message": msg}, 500

        return entry.json(), 201


class EntriesSearch(Resource):

    @jwt_required()
    @check('entries_search')
    @swag_from('../swagger/entries/search_entries.yaml')
    def post(self):
        query = EntriesModel.query
        query = query.join(MedicineModel, and_(EntriesModel.medicine_id == MedicineModel.id), isouter=True)
        query = query.join(ManufacturerModel, and_(EntriesModel.manufacturer_id == ManufacturerModel.id), isouter=True)
        query = query.join(SupplierModel, and_(EntriesModel.supplier_id == SupplierModel.id), isouter=True)
        query = query.join(DepositModel, and_(EntriesModel.deposit_id == DepositModel.id), isouter=True)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            or_filter_list = restrict_collector(or_filter_list, filters, 'medicine', lambda x: func.lower(
                MedicineModel.code + " - " + MedicineModel.description
            ).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'quantity', lambda x: cast(EntriesModel.quantity, sqlalchemy.String) == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'manufacturer', lambda x: func.lower(
                ManufacturerModel.name).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'supplier', lambda x: func.lower(
                SupplierModel.name).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'deposit', lambda x: func.lower(
                DepositModel.name).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'lot', lambda x: func.lower(
                EntriesModel.num_lot).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'expiration_date', lambda x: func.to_char(EntriesModel.expiration_date, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'origin', lambda x: func.lower(EntriesModel.origin).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
