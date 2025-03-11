import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask_babel import _

from db import db
from models.deposit_lot import DepositLotModel
from models.deposit_stock import DepositStockModel
from models.history import HistoryModel, EventCode
from models.lot import LotModel
from models.stock import StockModel
from security import check
from utils import restrict, paginated_results


class DepositStock(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('deposit_id', type=int)
    parser.add_argument('stock_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('observation', type=str)

    @jwt_required()
    @check('deposit_stock_get')
    @swag_from('../swagger/deposit_stock/get_deposit_stock.yaml')
    def get(self, id):
        deposit_stock = DepositStockModel.find_by_id(id)
        if deposit_stock:
            return deposit_stock.json()
        return {'message': _("DEPOSIT_STOCK_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_stock_update')
    @swag_from('../swagger/deposit_stock/put_deposit_stock.yaml')
    def put(self, id):
        deposit_stock = DepositStockModel.find_by_id(id)
        if deposit_stock:
            deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposit_stock.id).first()
            newdata = DepositStock.parser.parse_args()

            try:
                with db.session.no_autoflush:
                    # Se obtiene el stock del medicamento
                    stock = StockModel.query.filter_by(id=deposit_stock.stock_id).first()
                    if stock:
                        stock_delta = deposit_stock.quantity - newdata['quantity']
                        stock.quantity -= stock_delta
                        if stock.quantity < 0:
                            raise Exception(_("DEPOSIT_STOCK_0"))
                        db.session.add(stock)
                    else:
                        raise Exception(_("DEPOSIT_STOCK_NOT_FOUND"))

                    observation = newdata['observation']
                    del newdata['observation']
                    DepositStockModel.from_reqparse(deposit_stock, newdata)

                    if deposit_lot:
                        deposit_lot.quantity = deposit_stock.quantity
                        db.session.add(deposit_lot)

                    num_lot = LotModel.query.filter_by(id=deposit_lot.lote_id).first()

                    # Se registra en historial
                    historial = HistoryModel()
                    historial.orig_deposit_stock = deposit_stock
                    historial.quantity = -stock_delta
                    historial.event_id = HistoryModel.get_event(EventCode.AJUST_STOCK)
                    historial.description = observation
                    historial.user_create = get_jwt_identity()
                    historial.num_lot = num_lot.num_lot
                    db.session.add(historial)

                    db.session.add(deposit_stock)
                    # Se persisiten todos los cambios
                    db.session.commit()

                    return deposit_stock.json()
            except Exception as error:
                # Se revierte los cambios
                db.session.rollback()
                logging.error(error, exc_info=error)
                return {"message": error.__cause__}, 500

        return {'message': _("DEPOSIT_STOCK_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_stock_delete')
    @swag_from('../swagger/deposit_stock/delete_deposit_stock.yaml')
    def delete(self, id):
        deposit_stock = DepositStockModel.find_by_id(id)
        if deposit_stock:
            deposit_stock.delete_from_db()

        return {'message': _("DEPOSIT_STOCK_DELETED")}


class DepositStockList(Resource):

    @jwt_required()
    @check('deposit_stock_list')
    @swag_from('../swagger/deposit_stock/list_deposit_stock.yaml')
    def get(self):
        query = DepositStockModel.query
        return paginated_results(query)

    @jwt_required()
    @check('deposit_stock_insert')
    @swag_from('../swagger/deposit_stock/post_deposit_stock.yaml')
    def post(self):
        data = DepositStock.parser.parse_args()

        id = data.get('id')

        if id is not None and DepositStockModel.find_by_id(id):
            return {'message': _("DEPOSIT_STOCK_DUPLICATED").format(id)}, 400

        deposit_stock = DepositStockModel(**data)
        try:
            deposit_stock.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating deposit stock.', exc_info=e)
            return {"message": _("DEPOSIT_STOCK_CREATE_ERROR")}, 500

        return deposit_stock.json(), 201


class DepositStockSearch(Resource):

    @jwt_required()
    @check('deposit_stock_search')
    @swag_from('../swagger/deposit_stock/search_deposit_stock.yaml')
    def post(self):
        query = DepositStockModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: DepositStockModel.id == x)
            query = restrict(query, filters, 'deposit_id', lambda x: DepositStockModel.deposit_id == x)
            query = restrict(query, filters, 'stock_id', lambda x: DepositStockModel.stock_id == x)
        return paginated_results(query)
