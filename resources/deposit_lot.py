import logging

from flasgger import swag_from
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy import and_, or_, func

from models.deposit_lot import DepositLotModel
from models.lot import LotModel
from security import check
from utils import restrict, paginated_results, restrict_collector


class DepositLot(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('deposit_stock_id', type=int)
    parser.add_argument('lote_id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('quantity', type=int)

    @jwt_required()
    @check('deposit_lot_get')
    @swag_from('../swagger/deposit_lot/get_deposit_lot.yaml')
    def get(self, id):
        deposit_lot = DepositLotModel.find_by_id(id)
        if deposit_lot:
            return deposit_lot.json()
        return {'message': _("DEPOSIT_LOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_lot_update')
    @swag_from('../swagger/deposit_lot/put_deposit_lot.yaml')
    def put(self, id):
        deposit_lot = DepositLotModel.find_by_id(id)
        if deposit_lot:
            newdata = DepositLot.parser.parse_args()
            DepositLotModel.from_reqparse(deposit_lot, newdata)
            deposit_lot.save_to_db()
            return deposit_lot.json()
        return {'message': _("DEPOSIT_LOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_lot_delete')
    @swag_from('../swagger/deposit_lot/delete_deposit_lot.yaml')
    def delete(self, id):
        deposit_lot = DepositLotModel.find_by_id(id)
        if deposit_lot:
            deposit_lot.delete_from_db()

        return {'message': _("DEPOSIT_LOT_DELETED")}


class DepositLotList(Resource):

    @jwt_required()
    @check('deposit_lot_list')
    @swag_from('../swagger/deposit_lot/list_deposit_lot.yaml')
    def get(self):
        query = DepositLotModel.query
        return paginated_results(query)

    @jwt_required()
    @check('deposit_lot_insert')
    @swag_from('../swagger/deposit_lot/post_deposit_lot.yaml')
    def post(self):
        data = DepositLot.parser.parse_args()

        id = data.get('id')

        if id is not None and DepositLotModel.find_by_id(id):
            return {'message': _("DEPOSIT_LOT_DUPLICATED").format(id)}, 400

        deposit_lot = DepositLotModel(**data)
        try:
            deposit_lot.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating deposit lot.', exc_info=e)
            return {"message": _("DEPOSIT_LOT_CREATE_ERROR")}, 500

        return deposit_lot.json(), 201


class DepositLotSearch(Resource):

    @jwt_required()
    @check('deposit_lot_search')
    @swag_from('../swagger/deposit_lot/search_deposit_lot.yaml')
    def post(self):
        query = DepositLotModel.query

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: DepositLotModel.id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'deposit_stock_id',
                                                lambda x: DepositLotModel.deposit_stock_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'lote_id',
                                                lambda x: DepositLotModel.lote_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'quantity',
                                                lambda x: DepositLotModel.quantity == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'medicine_id',
                                                lambda x: DepositLotModel.medicine_id == x)

            lot_medicine = filters.get('filter_deposit_medicine_lot')
            if 'filter_deposit_medicine_lot' in filters and lot_medicine:
                print(filters.get('filter_deposit_medicine_lot'))
                query = query.filter(DepositLotModel.lote_id == lot_medicine.get('lote_id'))
                query = query.filter(DepositLotModel.medicine_id == lot_medicine.get('medicine_id'))

            lot_medicine_stock = filters.get('filter_medicine_lot')
            if 'filter_medicine_lot' in filters and lot_medicine_stock:
                print(filters.get('filter_medicine_lot'))
                query = query.filter(DepositLotModel.lote_id == lot_medicine_stock.get('lote_id'))
                query = query.filter(DepositLotModel.medicine_id == lot_medicine_stock.get('stock').get('medicine_id'))
            if 'depositStockId' in filters:
                # Preparar el filtro en el formato que acepta el selector
                result = (
                    query
                    .join(LotModel).filter(DepositLotModel.deposit_stock_id == filters.get('depositStockId'))
                    .with_entities(
                        DepositLotModel.lote_id,
                        LotModel.num_lot,
                        func.sum(DepositLotModel.quantity).label('total_quantity')
                    )
                    .group_by(DepositLotModel.lote_id, LotModel.num_lot)
                    .all()
                )
                response = [{'lote_id': lote_id, 'lot_name': num_lot, 'total_quantity': total_quantity}
                            for lote_id, num_lot, total_quantity in result]
                return jsonify(response)

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)


class DepositLotQuantitySearch(Resource):
    @jwt_required()
    @check('deposit_lot_search')
    @swag_from('../swagger/deposit_lot/search_deposit_lot.yaml')
    def post(self):
        query = DepositLotModel.query
        filters = request.json
        # Agrupar por lote_id y sumar las cantidades
        result = (
            query
            .join(LotModel).filter(DepositLotModel.medicine_id == filters.get('filter_medicine_stock'))
            .with_entities(
                DepositLotModel.lote_id,
                LotModel.num_lot,
                func.sum(DepositLotModel.quantity).label('total_quantity')
            )
            .group_by(DepositLotModel.lote_id, LotModel.num_lot)
            .all()
        )

        response = [{'lote_id': lote_id, 'lot_name': num_lot, 'total_quantity': total_quantity}
                    for lote_id, num_lot, total_quantity in result]

        return jsonify(response)
