import logging
from datetime import datetime
from operator import and_

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func
from sqlalchemy.orm import aliased
from flask_babel import _

from dao.interoperabilidad_dao import InteroperabilidadDao
from models.deposit_stock import DepositStockModel
from models.history import HistoryModel
from models.medicine import MedicineModel
from models.parameter import ParameterModel
from models.stock import StockModel
from security import check
from utils import restrict, paginated_results

class History(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('deposit_stock_id', type=int)
    parser.add_argument('dest_deposit_stock_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('description', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('stock_id', type=int)
    parser.add_argument('event_id', type=int)
    parser.add_argument('event', type=int)
    parser.add_argument('origin', type=str)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('observation', type=str)
    parser.add_argument('balance', type=float)
    parser.add_argument('original_quantity', type=float)
    parser.add_argument('num_lot', type=str)

    @jwt_required()
    @check('history_get')
    @swag_from('../swagger/history/get_history.yaml')
    def get(self, id):
        history = HistoryModel.find_by_id(id)
        if history:
            return history.json()
        return {'message': _("HISTORY_NOT_FOUND")}, 404

    @jwt_required()
    @check('history_update')
    @swag_from('../swagger/history/put_history.yaml')
    def put(self, id):
        history = HistoryModel.find_by_id(id)
        if history:
            newdata = History.parser.parse_args()
            HistoryModel.from_reqparse(history, newdata)
            history.save_to_db()
            return history.json()
        return {'message': _("HISTORY_NOT_FOUND")}, 404

    @jwt_required()
    @check('history_delete')
    @swag_from('../swagger/history/delete_history.yaml')
    def delete(self, id):
        history = HistoryModel.find_by_id(id)
        if history:
            history.delete_from_db()

        return {'message': _("HISTORY_DELETED")}


class HistoryList(Resource):

    @jwt_required()
    @check('history_list')
    @swag_from('../swagger/history/list_history.yaml')
    def get(self):
        query = HistoryModel.query
        return paginated_results(query)

    @jwt_required()
    @check('history_insert')
    @swag_from('../swagger/history/post_history.yaml')
    def post(self):
        data = History.parser.parse_args()

        id = data.get('id')

        if id is not None and HistoryModel.find_by_id(id):
            return {'message': _("HISTORY_DUPLICATED").format(id)}, 400

        history = HistoryModel(**data)
        try:
            history.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating history.', exc_info=e)
            return {"message": _("HISTORY_CREATE_ERROR")}, 500

        return history.json(), 201


class HistorySearch(Resource):

    @jwt_required()
    @check('history_search')
    @swag_from('../swagger/history/search_history.yaml')
    def post(self):
        query = HistoryModel.query
        orig_deposit_stock = aliased(DepositStockModel)
        query = query.join(orig_deposit_stock, HistoryModel.orig_deposit_stock_id == orig_deposit_stock.id, isouter=True)
        stock = aliased(StockModel)
        query = query.join(stock, orig_deposit_stock.stock_id == stock.id, isouter=True)
        event = aliased(ParameterModel)
        query = query.join(event, and_(HistoryModel.event_id == event.id,
                                       event.domain == 'STOCK_HISTORY_EVENT'), isouter=True)

        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: HistoryModel.id == x)
            query = restrict(query, filters, 'orig_deposit_stock_id', lambda x: HistoryModel.orig_deposit_stock_id == x)
            query = restrict(query, filters, 'dest_deposit_stock_id', lambda x: HistoryModel.dest_deposit_stock_id == x)
            query = restrict(query, filters, 'description', lambda x: HistoryModel.description.contains(x))
            query = restrict(query, filters, 'user', lambda x: HistoryModel.user.contains(x))
            query = restrict(query, filters, 'origin', lambda x: HistoryModel.origin.contains(x))
            query = restrict(query, filters, 'observation', lambda x: HistoryModel.observation.contains(x))
            query = restrict(query, filters, 'num_lot', lambda x: HistoryModel.num_lot.contains(x))

            # Relationship Filter
            query = restrict(query, filters, 'stock_id', lambda x: stock.id == x)
            query = restrict(query, filters, 'event', lambda x: func.lower(event.value).contains(func.lower(x)))

        return paginated_results(query)


class NewHistoryList(Resource):
    @jwt_required()
    @check('history_get')
    @swag_from('../swagger/history/get_history.yaml')
    def get(self, stock_id):
        stock: StockModel = StockModel.find_by_id(id=stock_id)
        medicine: MedicineModel = MedicineModel.find_by_id(id=stock.medicine_id)

        interoperabilidad_dao = InteroperabilidadDao()

        # CCAN
        # Listado ccan
        history_list_ccan = []
        medicine_ccan_header_list = interoperabilidad_dao.get_medicine_history_ccan_header(codigo_medicamento=medicine.code)
        medicine_ccan_mov_list = interoperabilidad_dao.get_medicine_history_ccan(codigo_medicamento=medicine.code)
        for medicine_ccan_mov in medicine_ccan_mov_list:
            ccan_mov = {
                'origin': medicine_ccan_mov.get('origin'),
                'date': medicine_ccan_mov.get('date').strftime("%Y-%m-%dT%H:%M:%S.%f"),
                'description': medicine_ccan_mov.get('description'),
                'observation': medicine_ccan_mov.get('observation'),
                'origen_codigo': medicine_ccan_mov.get('origen_codigo'),
                'origen_tipo': medicine_ccan_mov.get('origen_tipo'),
                'origen_nombre': medicine_ccan_mov.get('origen_nombre'),
                'destino_codigo': medicine_ccan_mov.get('destino_codigo'),
                'destino_tipo': medicine_ccan_mov.get('destino_tipo'),
                'destino_nombre': medicine_ccan_mov.get('destino_nombre'),
                'quantity': medicine_ccan_mov.get('original_quantity') if medicine_ccan_mov.get(
                    'original_quantity') else abs(medicine_ccan_mov.get('quantity')),
                'quantity_procesed': medicine_ccan_mov.get('quantity'),
                'numero_lote': medicine_ccan_mov.get('numero_lote'),
                'origen_interoperabilidad': medicine_ccan_mov.get('origen_interoperabilidad'),
            }
            history_list_ccan.append(ccan_mov)

        history_by_deposit_ccan = []
        # Group by deposit and lot
        for mov_dep_lot in medicine_ccan_header_list:
            codigo = mov_dep_lot.get('origen_codigo')
            dep = next((hist for hist in history_by_deposit_ccan if hist.get('deposit').get('codigo') == codigo), None)
            numero_lote = mov_dep_lot.get('numero_lote')
            lote_obj = {
                'numero_lote': numero_lote,
                'movements': sorted([mov for mov in history_list_ccan if
                                     mov.get('origen_codigo') == codigo and mov.get('numero_lote') == numero_lote],
                                    key=lambda x: x.get('date'))
            }
            if dep:
                dep['lot_list'].append(lote_obj)
            else:
                # Se agrega el depósito
                history_by_deposit_ccan.append({
                    'deposit': {
                        'codigo': mov_dep_lot.get('origen_codigo'),
                        'tipo': mov_dep_lot.get('origen_tipo'),
                        'nombre': mov_dep_lot.get('origen_nombre')
                    },
                    'lot_list': [lote_obj]
                })

        # Ajuste de balance por grupo
        for dep in history_by_deposit_ccan:
            for lote in dep.get('lot_list', []):
                balance = 0
                for mov in lote.get('movements', []):
                    mov['balance'] = mov['quantity_procesed'] + balance
                    balance = mov['balance']

        # Filtrar depósitos y lotes que no tienen movimientos
        history_by_deposit_ccan = [
            dep for dep in history_by_deposit_ccan
            if any(len(lote.get('movements', [])) > 0 for lote in dep.get('lot_list', []))
        ]

        for dep in history_by_deposit_ccan:
            dep['lot_list'] = [lote for lote in dep.get('lot_list', []) if len(lote.get('movements', [])) > 0]

        # Resume
        # CCAN
        total_stock_ccan = 0
        for dep in history_by_deposit_ccan:
            dep['total'] = 0
            for lote in dep.get('lot_list', []):
                lote['total'] = 0
                if len(lote.get('movements', [])) > 0:
                    last_mov = lote['movements'][-1]
                    lote['total'] = last_mov.get('balance')
                    dep['total'] += lote['total']
            total_stock_ccan += dep['total']

        # return_data
        return_data = {
            'ccan': {
                'total_stock': total_stock_ccan,
                'deposits': history_by_deposit_ccan
            }
        }

        return return_data
