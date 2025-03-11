import base64
import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import aliased

from models.deposit_stock import DepositStockModel
from models.entries import EntriesModel
from models.entries_deposit_stock import EntriesDepositStockModel
from models.history import HistoryModel, EventCode
from models.medicine import MedicineModel
from models.parameter import ParameterModel
from models.stock import StockModel
from security import check
from utils import restrict, paginated_results, restrict_collector, sorting_relationship_type, \
    sorting_relationship_type_by_two_columns
from db import db


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
    if not 'id' in entries:
        entries['id'] = None


def add_entries_to_deposit_stock(entries):
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
    deposito_stock_new = DepositStockModel.query.filter_by(deposit_id=entries.deposit_id,
                                                           stock_id=stock.id).first()
    # db.session.add(deposito_stock_new)
    add_entries_deposit_stock(entries, deposito_stock)

    # Se registra en historial
    historial = HistoryModel()
    historial.orig_deposit_stock = deposito_stock
    historial.quantity = entries.quantity
    historial.event_id = HistoryModel.get_event(EventCode.ADD_BY_LOTE)
    historial.description = f"Add by stock id {stock.id}"
    historial.user_create = get_jwt_identity()
    db.session.add(historial)


def add_entries_deposit_stock(entries, deposit_stock):
    if deposit_stock:
        entries_deposit_stock = EntriesDepositStockModel()
        entries_deposit_stock.entries_id = entries.id
        entries_deposit_stock.deposit_stock_id = deposit_stock.id
        db.session.add(entries_deposit_stock)
        db.session.commit()
    else:
        # Manejar el caso cuando deposit_stock es None
        print("Could not find deposit_stock.")


def delete_entries_deposit_stock(entries):
    # Se obtiene el stock del medicamento
    stock = StockModel.query.filter_by(medicine_id=entries.medicine_id).first()

    # Se obtiene el deposito stock
    if stock:
        deposito_stock = DepositStockModel.query.filter_by(deposit_id=entries.deposit_id,
                                                           stock_id=stock.id).first()
        if deposito_stock:
            final_quantity = deposito_stock.quantity - entries.quantity
            if final_quantity >= 0:
                deposito_stock.quantity = final_quantity
                stock.quantity -= entries.quantity

                # delete_entries_deposit_stock(entries, deposito_stock)
                entries_deposit_stock = EntriesDepositStockModel.query.filter_by(entries_id=entries.id, deposit_stock_id=deposito_stock.id)
                if entries_deposit_stock:
                    db.session.delete(entries_deposit_stock)

                # Se registra en historial
                historial = HistoryModel()
                historial.orig_deposit_stock = deposito_stock
                historial.quantity = -entries.quantity
                historial.event_id = HistoryModel.get_event(EventCode.REMOVE_BY_LOTE)
                historial.description = f"Add by stock id {stock.id}"
                historial.user_create = get_jwt_identity()
                db.session.add(historial)
            else:
                raise Exception('The stock entry cannot be deleted because the ending stock is less than zero')
        else:
            raise Exception('Stock_deposit does not exist')
    else:
        raise Exception('The stock of the medicine cannot be found')


def update_entries_to_deposit_stock(entries_new, entries_old):
    # Verificar si ha cambiado la medicina, el deposito o la cantidad
    change = False
    if entries_new.medicine_id != entries_old.medicine_id:
        change = True
    if entries_new.deposit_id != entries_old.deposit_id:
        change = True
    if entries_new.quantity != entries_old.quantity:
        change = True

    if change:
        delete_entries_deposit_stock(entries_old)
        add_entries_to_deposit_stock(entries_new)


class Stock(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('state_id', type=int)
    parser.add_argument('entries_list', type=list, location='json')

    @jwt_required()
    @check('stock_get')
    @swag_from('../swagger/stock/get_stock.yaml')
    def get(self, id):
        stock = StockModel.find_by_id(id)
        if stock:
            return stock.json()
        return {'message': _("STOCK_NOT_FOUND")}, 404

    @jwt_required()
    @check('stock_update')
    @swag_from('../swagger/stock/put_stock.yaml')
    def put(self, id):
        """stock = StockModel.find_by_id(id)
        if stock:
            newdata = Stock.parser.parse_args()
            StockModel.from_reqparse(stock, newdata)
            stock.save_to_db()
            return stock.json()
        return {'message': 'No se encuentra Stock'}, 404"""

        stock = StockModel.find_by_id(id)
        if stock:
            newdata = Stock.parser.parse_args()
            entries_list = newdata['entries_list'] if newdata['entries_list'] is not None else []
            del newdata['entries_list']
            StockModel.from_reqparse(stock, newdata)
            entries_id_old = [entries.id for entries in stock.entries_list]
            entries_id_new = [entries['id'] for entries in entries_list if 'id' in entries]
            entries_id_delete = list(set(entries_id_old) - set(entries_id_new))
            entries_id_update = list(set(entries_id_new) - set(entries_id_delete))
            entries_delete_list = [entries for entries in stock.entries_list if entries.id in entries_id_delete]
            entries_update_list_old = [entries for entries in stock.entries_list if entries.id in entries_id_update]
            entries_update_list_new = [entries for entries in entries_list if
                                       'id' in entries and entries['id'] in entries_id_update]
            entries_add_list = [entries for entries in entries_list if 'id' not in entries or entries['id'] is None]

            try:
                with db.session.no_autoflush:
                    # Se registra el detalle del lote
                    entries_list_update = []

                    # New
                    for new_entry in entries_add_list:
                        clean_entries(new_entry)
                        entries_model = EntriesModel(**new_entry)

                        entries_list_update.append(entries_model)
                        # Se actualiza el stock vía el detalle
                        add_entries_to_deposit_stock(new_entry)

                    # Delete
                    for entries in entries_delete_list:
                        delete_entries_deposit_stock(entries)
                        db.session.delete(entries)

                    # Update
                    for entries_old in entries_update_list_old:
                        # Obtener el elemento nuevo para comparar con el anterior
                        lot_detail_new_dict = next(
                            x for x in entries_update_list_new if x['id'] == entries_old.id)
                        clean_entries(lot_detail_new_dict)
                        entries_new = EntriesModel(**lot_detail_new_dict)

                        # Se Ajusta Stock
                        update_entries_to_deposit_stock(entries_new, entries_old)

                        # Cambios del Lot Detail
                        entries_old.medicine_id = entries_new.medicine_id
                        entries_old.quantity = entries_new.quantity
                        entries_old.deposit_id = entries_new.deposit_id
                        entries_old.description = entries_new.description
                        entries_old.expiration_date = entries_new.expiration_date
                        entries_old.manufacturer_id = entries_new.manufacturer_id
                        entries_old.manufacturing_date = entries_new.manufacturing_date
                        entries_old.supplier_id = entries_new.supplier_id
                        entries_old.observation = entries_new.observation
                        entries_old.storage_conditions = entries_new.storage_conditions

                        # Se persiste el detalle del lote
                        entries_list_update.append(entries_old)

                    stock.entries_list = entries_list_update

                    # Se persisiten todos los cambios
                    db.session.commit()
            except Exception as error:
                # Se revierte los cambios
                db.session.rollback()
                msg = "An error occurred while updating the Stock."
                logging.error(msg, exc_info=error)
                return {"message": msg}, 500

            return stock.json()
        return {'message': _("STOCK_NOT_FOUND")}, 404

    @jwt_required()
    @check('stock_delete')
    @swag_from('../swagger/stock/delete_stock.yaml')
    def delete(self, id):
        stock = StockModel.find_by_id(id)
        if stock:
            stock.delete_from_db()

        return {'message': _("STOCK_DELETED")}


class StockList(Resource):

    @jwt_required()
    @check('stock_list')
    @swag_from('../swagger/stock/list_stock.yaml')
    def get(self):
        query = StockModel.query
        return paginated_results(query)

    @jwt_required()
    @check('stock_insert')
    @swag_from('../swagger/stock/post_stock.yaml')
    def post(self):
        data = Stock.parser.parse_args()

        id = data.get('id')

        if id is not None and StockModel.find_by_id(id):
            return {'message': _("STOCK_DUPLICATED").format(id)}, 400

        try:
            with db.session.no_autoflush:
                lot_detail_list = data['entries_list']
                del data['entries_list']
                stock = StockModel(**data)
                stock_state_active = ParameterModel.query.filter_by(domain='STOCK_STATE', code='A').first()
                if stock_state_active:
                    stock.state_id = stock_state_active.id

                # Se registra el detalle del lote
                for entries in lot_detail_list:
                    clean_entries(entries)
                    entries_model = EntriesModel(**entries)
                    stock.entries_list.append(entries_model)
                    # Se actualiza el stock vía el detalle
                    add_entries_to_deposit_stock(entries_model)

                # Se persisiten todos los cambios
        except Exception as error:
            # Se revierte los cambios
            db.session.rollback()
            msg = "An error occurred while creating the Stock."
            logging.error(msg, exc_info=error)
            return {"message": msg}, 500

        return stock.json(), 201


class StockSearch(Resource):

    @jwt_required()
    @check('stock_search')
    @swag_from('../swagger/stock/search_stock.yaml')
    def post(self):
        # Se verifica si hay nuevos medicamentos para control
        checkControlStock()

        query = StockModel.query

        # Relationship
        medicine = aliased(MedicineModel)
        query = query.join(medicine, StockModel.medicine_id == medicine.id)

        state = aliased(ParameterModel)
        query = query.join(state, StockModel.state_id == state.id)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            # query = restrict(query, filters, 'id', lambda x: StockModel.id == x)
            # query = restrict(query, filters, 'medicine_id', lambda x: StockModel.medicine_id == x)
            # query = restrict(query, filters, 'state_id', lambda x: StockModel.state_id == x)

            # Relationship Filter
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(medicine.code).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'generic_name', lambda x: func.lower(medicine.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'generic_name', lambda x: func.lower(medicine.generic_name).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'concentration',
                                                lambda x: func.lower(medicine.concentration).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'pharmaceutical_form',
                                                lambda x: func.lower(medicine.pharmaceutical_form).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'presentation',
                                                lambda x: func.lower(medicine.presentation).contains(func.lower(x)))
            if 'medicine_id' in filters and filters.get('medicine_id'):
                query = query.filter(StockModel.medicine_id == filters.get('medicine_id'))

            # or_filter_list = restrict_collector(or_filter_list, filters, 'state', lambda x: func.lower(state.value).contains(func.lower(x)))

            # Apply filters
            general_filter = request.args.get('general_filter', None, str) == 'true'
            if general_filter:
                query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
            else:
                filter_list = and_filter_list + or_filter_list
                query = query.filter(and_(*filter_list))

        # Capture Relationship Sorting and configure performance
        sort = True
        sort_by = request.args.get('sortBy', None, str)
        if sort_by:
            if sort_by == 'code':
                query = sorting_relationship_type(request, query, medicine.code)
                sort = False
            elif sort_by == 'generic_name':
                query = sorting_relationship_type_by_two_columns(request, query, medicine.generic_name, medicine.description)
                sort = False
            elif sort_by == 'concentration':
                query = sorting_relationship_type(request, query, medicine.concentration)
                sort = False
            elif sort_by == 'pharmaceutical_form':
                query = sorting_relationship_type(request, query, medicine.pharmaceutical_form)
                sort = False
            elif sort_by == 'presentation':
                query = sorting_relationship_type(request, query, medicine.presentation)
                sort = False
            # elif sort_by == 'state':
            #     query = sorting_relationship_type(request, query, state.value)
            #     sort = False

        return paginated_results(query, sort)


def checkControlStock():
    """
    Método encargado de agregar al stock los medicamentos en seguimiento
    """
    try:
        medicine_control_list = MedicineModel.query.filter_by(stock_control=True).all()
        medicine_control_list_id = list(map(lambda x: x.id, medicine_control_list))

        stock_list = StockModel.query.all()
        stock_list_medicine_ids = list(map(lambda x: x.medicine_id, stock_list))

        medicine_to_add = list(set(medicine_control_list_id) - set(stock_list_medicine_ids))
        with db.session.no_autoflush:
            stock_state_active = ParameterModel.query.filter_by(domain='STOCK_STATE', code='A').first()
            for medicine_id in medicine_to_add:
                stock: StockModel = StockModel()
                stock.medicine_id = medicine_id
                stock.quantity = 0
                stock.state_id = stock_state_active.id

                # Se persisten los cambios
                db.session.add(stock)

            db.session.commit()
    except Exception as error:
        # Se revierte los cambios
        db.session.rollback()
