import logging
from datetime import datetime

import sqlalchemy
from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy import func, and_, or_, cast
from sqlalchemy.orm import aliased

from db import db
from models.deposit import DepositModel
from models.deposit_lot import DepositLotModel
from models.deposit_movement import DepositMovementModel
from models.deposit_stock import DepositStockModel
from models.history import HistoryModel, EventCode
from models.lot import LotModel
from models.medicine import MedicineModel
from security import check
from utils import restrict, paginated_results, restrict_collector, sorting_relationship_type


class DepositMovement(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('deposit_stock_in_id', type=int)
    parser.add_argument('deposit_stock_out_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('deposit_in_id', type=int)
    parser.add_argument('lote_id', type=int)

    @jwt_required()
    @check('deposit_movement_get')
    @swag_from('../swagger/deposit_movement/get_deposit_movement.yaml')
    def get(self, id):
        deposit_movement = DepositMovementModel.find_by_id(id)
        if deposit_movement:
            return deposit_movement.json()
        return {'message': _("DEPOSIT_MOVEMENT_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_movement_update')
    @swag_from('../swagger/deposit_movement/put_deposit_movement.yaml')
    def put(self, id):
        deposit_movement = DepositMovementModel.find_by_id(id)
        if deposit_movement:
            newdata = DepositMovement.parser.parse_args()
            DepositMovementModel.from_reqparse(deposit_movement, newdata)
            deposit_movement.save_to_db()
            return deposit_movement.json()
        return {'message': _("DEPOSIT_MOVEMENT_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_movement_delete')
    @swag_from('../swagger/deposit_movement/delete_deposit_movement.yaml')
    def delete(self, id):
        deposit_movement = DepositMovementModel.find_by_id(id)
        if deposit_movement:
            deposit_movement.delete_from_db()

        return {'message': _("DEPOSIT_MOVEMENT_DELETED")}


class DepositMovementList(Resource):

    @jwt_required()
    @check('deposit_movement_list')
    @swag_from('../swagger/deposit_movement/list_deposit_movement.yaml')
    def get(self):
        query = DepositMovementModel.query
        return paginated_results(query)

    @jwt_required()
    @check('deposit_movement_insert')
    @swag_from('../swagger/deposit_movement/post_deposit_movement.yaml')
    def post(self):
        data = DepositMovement.parser.parse_args()

        id = data.get('id')

        if id is not None and DepositMovementModel.find_by_id(id):
            return {'message': _("DEPOSIT_MOVEMENT_DUPLICATED").format(id)}, 400

        deposit_in_id = data['deposit_in_id']
        del data['deposit_in_id']
        deposit_movement = DepositMovementModel(**data)
        deposit_movement.date_create = datetime.now()
        deposit_movement.user_create = get_jwt_identity()

        try:
            with db.session.no_autoflush:
                # Obtener el deposito stock de entrada
                deposit_stock_out = DepositStockModel.find_by_id(id=deposit_movement.deposit_stock_out_id)
                deposit_stock_in = DepositStockModel.query.filter_by(deposit_id=deposit_in_id,
                                                                     stock_id=deposit_stock_out.stock.id).first()
                # Obtener el deposit_lot si existe
                deposit_lot_out = DepositLotModel.query.filter_by(deposit_stock_id=deposit_movement.deposit_stock_out_id, lote_id=deposit_movement.lote_id).first()

                deposit_lot_in = DepositLotModel.query.filter_by(deposit_stock_id=deposit_movement.deposit_stock_in_id, lote_id=deposit_movement.lote_id).first()

                if not deposit_stock_in:
                    # Se crea el deposito stock
                    deposit_stock_in = DepositStockModel(id=None, deposit_id=deposit_in_id,
                                                         stock_id=deposit_stock_out.stock.id, quantity=0)

                deposit_stock_out.quantity -= deposit_movement.quantity
                db.session.add(deposit_stock_out)

                deposit_stock_in.quantity += deposit_movement.quantity
                db.session.add(deposit_stock_in)
                db.session.flush()

                if not deposit_lot_in:
                    deposit_lot_in = DepositLotModel(id=None, deposit_stock_id=deposit_stock_in.id,
                                                     lote_id=deposit_movement.lote_id,
                                                     medicine_id=deposit_stock_out.stock.medicine_id, quantity=0)

                deposit_lot_out.quantity -= int(deposit_movement.quantity)
                db.session.add(deposit_lot_out)

                deposit_lot_in.quantity += int(deposit_movement.quantity)
                db.session.add(deposit_lot_in)

                # Se asocia el deposit_stock de entrada
                deposit_movement.deposit_stock_in = deposit_stock_in
                db.session.add(deposit_movement)

                num_lot = LotModel.query.filter_by(id=deposit_movement.lote_id).first()

                # Se registra en el historial
                historial_out: HistoryModel = HistoryModel()
                historial_out.orig_deposit_stock = deposit_stock_out
                historial_out.dest_deposit_stock = deposit_stock_in
                historial_out.quantity = -deposit_movement.quantity
                historial_out.event_id = HistoryModel.get_event(EventCode.DEPOSIT_MOV)
                historial_out.description = 'Deposit out'
                historial_out.user_create = get_jwt_identity()
                historial_out.num_lot = num_lot.num_lot
                db.session.add(historial_out)

                historial_in: HistoryModel = HistoryModel()
                historial_in.orig_deposit_stock = deposit_stock_in
                historial_in.dest_deposit_stock = deposit_stock_out
                historial_in.quantity = deposit_movement.quantity
                historial_in.event_id = HistoryModel.get_event(EventCode.DEPOSIT_MOV)
                historial_in.description = 'Deposit in'
                historial_in.user_create = get_jwt_identity()
                historial_in.num_lot = num_lot.num_lot
                db.session.add(historial_in)

                # Se persisiten todos los cambios
                db.session.commit()
        except Exception as error:
            # Se revierte los cambios
            db.session.rollback()
            msg = _("DEPOSIT_MOVEMENT_CREATE_ERROR")
            logging.error(f"{msg}. Details: {error.__cause__}", exc_info=error)
            return {"message": f"{msg}. Details: {error.__cause__}"}, 500

        return deposit_movement.json(), 201


class DepositMovementSearch(Resource):

    @jwt_required()
    @check('deposit_movement_search')
    @swag_from('../swagger/deposit_movement/search_deposit_movement.yaml')
    def post(self):
        query = DepositMovementModel.query

        deposit_model_in = aliased(DepositModel)
        deposit_model_out = aliased(DepositModel)
        query = query.join(deposit_model_in, DepositMovementModel.deposit_stock_in_id == deposit_model_in.id, isouter=True)
        query = query.join(deposit_model_out, DepositMovementModel.deposit_stock_out_id == deposit_model_out.id,
                           isouter=True)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json

            # or_filter_list = restrict_collector(or_filter_list, filters, 'medicine', lambda x: func.lower(
            #     MedicineModel.code + " - " + MedicineModel.description
            # ).contains(func.lower(x)))

            or_filter_list = restrict_collector(or_filter_list, filters, 'quantity',
                                                lambda x: cast(DepositMovementModel.quantity, sqlalchemy.String) == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'lot', lambda x: func.lower(
                DepositMovementModel.num_lot).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_create',
                                                lambda x: func.to_char(DepositMovementModel.date_create,
                                                                       'DD/MM/YYYY HH24:MI:SS').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_create', lambda x: func.lower(
                DepositMovementModel.user_create).contains(func.lower(x)))

            or_filter_list = restrict_collector(or_filter_list, filters, 'deposit_stock_out_id_deposit_stock',
                                                lambda x: func.lower(
                                                    deposit_model_out.code + " - " + deposit_model_out.name).contains(
                                                    func.lower(x)))

            or_filter_list = restrict_collector(or_filter_list, filters, 'deposit_stock_in_id_deposit_stock',
                                                lambda x: func.lower(
                                                    deposit_model_in.code + " - " + deposit_model_in.name).contains(
                                                    func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list)).filter(or_(*or_filter_list))

        sort = True
        sort_by = request.args.get('sortBy', None, str)
        if sort_by:
            if sort_by == 'date_create':
                query = sorting_relationship_type(request, query, DepositMovementModel.date_create)
                sort = False
        return paginated_results(query,sort)
