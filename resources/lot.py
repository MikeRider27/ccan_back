import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from db import db
from models.deposit_lot import DepositLotModel
from models.deposit_stock import DepositStockModel
from models.entries import EntriesModel
from models.history import HistoryModel, EventCode
from models.lot import LotModel
from models.parameter import ParameterModel
from models.stock import StockModel
from security import check
from utils import restrict, paginated_results


def clean_entries(entries):
    if 'deposit' in entries:
        del entries['deposit']
    if 'medicine' in entries:
        del entries['medicine']
    if 'manufacturer' in entries:
        del entries['manufacturer']
    if 'supplier' in entries:
        del entries['supplier']
    if 'modify' in entries:
        del entries['modify']
    if 'lote' in entries:
        del entries['lote']


def add_lot_to_stock(entries, num_lot):
    # TODO: tener en cuenta el estado del medicamento y del stock
    # Se obtiene el stock del medicamento
    stock = StockModel.query.filter_by(medicine_id=entries.medicine_id).first()

    # Se obtiene el deposito stock
    deposito_stock = None
    if stock:
        deposito_stock = DepositStockModel.query.filter_by(deposit_id=entries.deposit_id,
                                                           stock_id=stock.id).first()
        stock.quantity += entries.quantity
        db.session.add(stock)
    else:
        stock_state = ParameterModel.query.filter_by(domain='STOCK_STATE', code='A').first()
        stock = StockModel(id=None, medicine_id=entries.medicine_id, quantity=entries.quantity,
                           state_id=stock_state.id)
        db.session.add(stock)
        db.session.flush()

    # Se actualiza el depósito stock
    if deposito_stock:
        deposito_stock.quantity += entries.quantity
    else:
        deposito_stock = DepositStockModel(id=None, deposit_id=entries.deposit_id,
                                           stock_id=stock.id, quantity=entries.quantity)
    db.session.add(deposito_stock)
    db.session.flush()

    # Obtener el deposit_lot si existe
    deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposito_stock.id, medicine_id=entries.medicine_id).first()

    # Se actualiza o agrega el deposit_lot
    if deposit_lot:
        deposit_lot.quantity += entries.quantity
    else:
        deposit_lot = DepositLotModel(id=None, deposit_stock_id=deposito_stock.id, lote_id=None,
                                      medicine_id=entries.medicine_id, quantity=entries.quantity)
    db.session.add(deposit_lot)

    # Se registra en historial
    historial = HistoryModel()
    historial.orig_deposit_stock = deposito_stock
    historial.quantity = entries.quantity
    historial.event_id = HistoryModel.get_event(EventCode.ADD_BY_LOTE)
    historial.description = f"Add by lot number {num_lot}"
    historial.user_create = get_jwt_identity()
    historial.num_lot = num_lot
    db.session.add(historial)


def delete_lot_to_stock(entries, num_lot):
    # Se obtiene el stock del medicamento
    stock = StockModel.query.filter_by(medicine_id=entries.medicine_id).first()

    # Se obtiene el depósito stock
    if stock:
        deposito_stock = DepositStockModel.query.filter_by(deposit_id=entries.deposit_id,
                                                           stock_id=stock.id).first()
        if deposito_stock:
            deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposito_stock.id, lote_id=entries.lote_id,
                                                          medicine_id=entries.medicine_id).first()
            final_quantity = deposito_stock.quantity - entries.quantity
            if final_quantity >= 0:
                deposito_stock.quantity = final_quantity
                deposit_lot.quantity = final_quantity
                stock.quantity -= entries.quantity
                db.session.delete(deposit_lot)
                # TODO VERIFICAR si esta persisistiendo los cambios
                # stock.save_to_db()
                # deposito_stock.save_to_db()

                # Se registra en historial
                historial = HistoryModel()
                historial.orig_deposit_stock = deposito_stock
                historial.quantity = -entries.quantity
                historial.event_id = HistoryModel.get_event(EventCode.REMOVE_BY_LOTE)
                historial.description = f"Delete lot number {num_lot}"
                historial.user_create = get_jwt_identity()
                historial.num_lot = num_lot
                db.session.add(historial)
            else:
                raise Exception(
                    _("LOT_NOT_DELETED"))
        else:
            raise Exception(_("DEPOSIT_STOCK_NOT_FOUND"))
    else:
        raise Exception(_("STOCK_NOT_FOUND"))


def update_lot_to_stock(lot_detail_new, lot_detail_old, num_lot):
    # Verificar si ha cambiado la medicina, el deposito o la cantidad
    change = False
    if lot_detail_new.medicine_id != lot_detail_old.medicine_id:
        change = True
    if lot_detail_new.deposit_id != lot_detail_old.deposit_id:
        change = True
    if lot_detail_new.quantity != lot_detail_old.quantity:
        change = True

    if change:
        delete_lot_to_stock(lot_detail_old, num_lot)
        add_lot_to_stock(lot_detail_new, num_lot)


class Lot(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('num_lot', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('entries_list', type=list, location='json')
    parser.add_argument('origin', type=str)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())

    @jwt_required()
    @check('lot_get')
    @swag_from('../swagger/lot/get_lot.yaml')
    def get(self, id):
        lot = LotModel.find_by_id(id)
        if lot:
            return lot.json()
        return {'message': _("LOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('lot_update')
    @swag_from('../swagger/lot/put_lot.yaml')
    def put(self, id):
        lot = LotModel.find_by_id(id)
        if lot:
            newdata = Lot.parser.parse_args()
            entries_list = newdata['entries_list'] if newdata['entries_list'] is not None else []
            del newdata['entries_list']
            LotModel.from_reqparse(lot, newdata)
            lot_detail_id_old = [detail.id for detail in lot.entries_list]
            lot_detail_id_new = [detail['id'] for detail in entries_list if 'id' in detail]
            lot_detail_id_delete = list(set(lot_detail_id_old) - set(lot_detail_id_new))
            lot_detail_id_update = list(set(lot_detail_id_new) - set(lot_detail_id_delete))
            lot_detail_delete_list = [detail for detail in lot.entries_list if detail.id in lot_detail_id_delete]
            lot_detail_update_list_old = [detail for detail in lot.entries_list if detail.id in lot_detail_id_update]
            lot_detail_update_list_new = [detail for detail in entries_list if
                                          'id' in detail and detail['id'] in lot_detail_id_update]
            lot_detail_add_list = [detail for detail in entries_list if 'id' not in detail or detail['id'] is None]

            try:
                with db.session.no_autoflush:
                    # Se registra el detalle del lote
                    lot_detail_list_update = []

                    # New
                    for new_detail in lot_detail_add_list:
                        clean_entries(new_detail)
                        lot_detail_model = EntriesModel(**new_detail)

                        lot_detail_list_update.append(lot_detail_model)
                        # Se actualiza el stock vía el detalle
                        add_lot_to_stock(lot_detail_model, lot.num_lot)
                        # add_lot_entries(lot_detail_model, lot)

                    # Delete
                    for delete_detail in lot_detail_delete_list:
                        delete_lot_to_stock(delete_detail, lot.num_lot)
                        db.session.delete(delete_detail)

                    # Update
                    for lot_detail_old in lot_detail_update_list_old:
                        # Obtener el elemento nuevo para comparar con el anterior
                        lot_detail_new_dict = next(x for x in lot_detail_update_list_new if x['id'] == lot_detail_old.id)
                        clean_entries(lot_detail_new_dict)
                        lot_detail_new = EntriesModel(**lot_detail_new_dict)

                        # Se Ajusta Stock
                        update_lot_to_stock(lot_detail_new, lot_detail_old, lot.num_lot)

                        # Cambios del Lot Detail
                        lot_detail_old.medicine_id = lot_detail_new.medicine_id
                        lot_detail_old.quantity = lot_detail_new.quantity
                        lot_detail_old.deposit_id = lot_detail_new.deposit_id
                        lot_detail_old.description = lot_detail_new.description
                        lot_detail_old.expiration_date = datetime.strptime(lot_detail_new.expiration_date, '%d/%m/%Y').date() if lot_detail_new.expiration_date else None
                        lot_detail_old.manufacturer_id = lot_detail_new.manufacturer_id
                        lot_detail_old.manufacturing_date = datetime.strptime(lot_detail_new.manufacturing_date, '%d/%m/%Y').date() if lot_detail_new.manufacturing_date else None
                        lot_detail_old.supplier_id = lot_detail_new.supplier_id
                        lot_detail_old.observation = lot_detail_new.observation
                        lot_detail_old.storage_conditions = lot_detail_new.storage_conditions

                        # Se persiste el detalle del lote
                        lot_detail_list_update.append(lot_detail_old)

                    lot.entries_list = lot_detail_list_update
                    lot.date_modify = datetime.now()
                    lot.user_modify = get_jwt_identity()
                    # Se persisiten todos los cambios
                    db.session.commit()

                    # Cargar el lote_id para las entradas recien creadas
                    EntriesModel.query.filter_by(lote_id=None).update({'lote_id': lot.id})

                    # Cargar el lote para deposit_lot
                    DepositLotModel.query.filter_by(lote_id=None).update({'lote_id': lot.id})
                    db.session.commit()
            except Exception as error:
                # Se revierte los cambios
                db.session.rollback()
                msg = _("LOT_UPDATE_ERROR")
                logging.error(msg, exc_info=error)
                return {"message": msg}, 500

            return lot.json()
        return {'message': _("LOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('lot_delete')
    @swag_from('../swagger/lot/delete_lot.yaml')
    def delete(self, id):
        lot = LotModel.find_by_id(id)
        if lot:
            lot.delete_from_db()

        return {'message': _("LOT_DELETED")}


class LotList(Resource):

    @jwt_required()
    @check('lot_list')
    @swag_from('../swagger/lot/list_lot.yaml')
    def get(self):
        query = LotModel.query
        return paginated_results(query)

    @jwt_required()
    @check('lot_insert')
    @swag_from('../swagger/lot/post_lot.yaml')
    def post(self):
        data = Lot.parser.parse_args()

        id = data.get('id')

        if id is not None and LotModel.find_by_id(id):
            return {'message': _("LOT_DUPLICATED").format(id)}, 400

        try:
            with db.session.no_autoflush:
                entries_list = data['entries_list']
                del data['entries_list']
                lot = LotModel(**data)

                # Se registra el detalle del lote
                for entry in entries_list:
                    clean_entries(entry)
                    entry_model = EntriesModel(**entry)

                    # Dates convert str to date
                    entry_model.expiration_date = datetime.strptime(entry.get('expiration_date'), '%d/%m/%Y').date() if entry.get('expiration_date') else None
                    entry_model.manufacturing_date = datetime.strptime(entry.get('manufacturing_date'), '%d/%m/%Y').date() if entry.get('manufacturing_date') else None
                    entry_model.date = datetime.strptime(entry.get('date'), '%d/%m/%Y').date() if entry.get('date') else None
                    lot.entries_list.append(entry_model)

                    # Se actualiza el stock vía el detalle
                    add_lot_to_stock(entry_model, lot.num_lot)

                lot.date_create = datetime.now()
                lot.user_create = get_jwt_identity()

                # Se persisiten todos los cambios
                db.session.add(lot)
                db.session.commit()

                # Cargar el lote_id para las entradas recien creadas
                EntriesModel.query.filter_by(lote_id=None).update({'lote_id': lot.id})

                # Cargar el lote para deposit_lot
                DepositLotModel.query.filter_by(lote_id=None).update({'lote_id': lot.id})
                db.session.commit()
        except Exception as error:
            # Se revierte los cambios
            db.session.rollback()
            msg = _("LOT_CREATE_ERROR")
            logging.error(msg, exc_info=error)
            return {"message": msg}, 500

        return lot.json(), 201


class LotSearch(Resource):

    @jwt_required()
    @check('lot_search')
    @swag_from('../swagger/lot/search_lot.yaml')
    def post(self):
        query = LotModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: LotModel.id == x)
            query = restrict(query, filters, 'num_lot', lambda x: LotModel.num_lot == x)
            query = restrict(query, filters, 'user_create', lambda x: LotModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: LotModel.user_modify.contains(x))
            query = restrict(query, filters, 'origin', lambda x: LotModel.origin.contains(x))
            query = restrict(query, filters, 'date', lambda x: func.to_char(LotModel.date, 'DD/MM/YYYY').contains(x))
        return paginated_results(query)
