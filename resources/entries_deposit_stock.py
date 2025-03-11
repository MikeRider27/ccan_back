import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.entries_deposit_stock import EntriesDepositStockModel
from utils import restrict, paginated_results
from security import check


class EntriesDepositStock(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('entries_id', type=int)
    parser.add_argument('deposit_stock_id', type=int)

    @jwt_required()
    @check('entries_deposit_stock_get')
    @swag_from('../swagger/entries_deposit_stock/get_entries_deposit_stock.yaml')
    def get(self, id):
        entries_deposit_stock = EntriesDepositStockModel.find_by_id(id)
        if entries_deposit_stock:
            return entries_deposit_stock.json()
        return {'message': _("ENTRIES_DEPOSIT_STOCK_NOT_FOUND")}, 404

    @jwt_required()
    @check('entries_deposit_stock_update')
    @swag_from('../swagger/entries_deposit_stock/put_entries_deposit_stock.yaml')
    def put(self, id):
        entries_deposit_stock = EntriesDepositStockModel.find_by_id(id)
        if entries_deposit_stock:
            newdata = EntriesDepositStock.parser.parse_args()
            EntriesDepositStockModel.from_reqparse(entries_deposit_stock, newdata)
            entries_deposit_stock.save_to_db()
            return entries_deposit_stock.json()
        return {'message': _("ENTRIES_DEPOSIT_STOCK_NOT_FOUND")}, 404

    @jwt_required()
    @check('entries_deposit_stock_delete')
    @swag_from('../swagger/entries_deposit_stock/delete_entries_deposit_stock.yaml')
    def delete(self, id):
        entries_deposit_stock = EntriesDepositStockModel.find_by_id(id)
        if entries_deposit_stock:
            entries_deposit_stock.delete_from_db()

        return {'message': _("ENTRIES_DEPOSIT_STOCK_DELETED")}


class EntriesDepositStockList(Resource):

    @jwt_required()
    @check('entries_deposit_stock_list')
    @swag_from('../swagger/entries_deposit_stock/list_entries_deposit_stock.yaml')
    def get(self):
        query = EntriesDepositStockModel.query
        return paginated_results(query)

    @jwt_required()
    @check('entries_deposit_stock_insert')
    @swag_from('../swagger/entries_deposit_stock/post_entries_deposit_stock.yaml')
    def post(self):
        data = EntriesDepositStock.parser.parse_args()

        id = data.get('id')

        if id is not None and EntriesDepositStockModel.find_by_id(id):
            return {'message': _("ENTRIES_DEPOSIT_STOCK_DUPLICATED").format(id)}, 400

        entries_deposit_stock = EntriesDepositStockModel(**data)
        try:
            entries_deposit_stock.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating entries deposit stock.', exc_info=e)
            return {"message": _("ENTRIES_DEPOSIT_STOCK_CREATE_ERROR")}, 500

        return entries_deposit_stock.json(), 201


class EntriesDepositStockSearch(Resource):

    @jwt_required()
    @check('entries_deposit_stock_search')
    @swag_from('../swagger/entries_deposit_stock/search_entries_deposit_stock.yaml')
    def post(self):
        query = EntriesDepositStockModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: EntriesDepositStockModel.id == x)
            query = restrict(query, filters, 'entries_id', lambda x: EntriesDepositStockModel.entries_id == x)
            query = restrict(query, filters, 'deposit_stock_id', lambda x: EntriesDepositStockModel.deposit_stock_id == x)

        # default order
        query = query.order_by(EntriesDepositStockModel.id.desc())
        return paginated_results(query)
