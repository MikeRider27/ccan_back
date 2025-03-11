import logging
from datetime import datetime

import sqlalchemy
from flasgger import swag_from
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func, cast, and_, or_
from flask_babel import _

from db import db
from models.deposit import DepositModel
from models.deposit_lot import DepositLotModel
from models.deposit_stock import DepositStockModel
from models.dispatch_medications import DispatchMedicationsModel
from models.history import HistoryModel, EventCode
from models.lot import LotModel
from models.medicine import MedicineModel
from models.patient import PatientModel
from models.stock import StockModel
from security import check
from utils import restrict, paginated_results, restrict_collector, apply_filters


class DispatchMedications(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('deposit_stock_id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('origin', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date',  type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('lote_id', type=int)
    @jwt_required()
    @check('dispatch_medications_get')
    @swag_from('../swagger/dispatch_medications/get_dispatch_medications.yaml')
    def get(self, id):
        dispatch_medications = DispatchMedicationsModel.find_by_id(id)
        if dispatch_medications:
            return dispatch_medications.json()
        return {'message': _("DISPATCH_MEDICATIONS_NOT_FOUND")}, 404

    @jwt_required()
    @check('dispatch_medications_update')
    @swag_from('../swagger/dispatch_medications/put_dispatch_medications.yaml')
    def put(self, id):
        dispatch_medications = DispatchMedicationsModel.find_by_id(id)
        if dispatch_medications:
            newdata = DispatchMedications.parser.parse_args()
            DispatchMedicationsModel.from_reqparse(dispatch_medications, newdata)
            dispatch_medications.save_to_db()
            return dispatch_medications.json()
        return {'message': _("DISPATCH_MEDICATIONS_NOT_FOUND")}, 404

    @jwt_required()
    @check('dispatch_medications_delete')
    @swag_from('../swagger/dispatch_medications/delete_dispatch_medications.yaml')
    def delete(self, id):
        dispatch_medications = DispatchMedicationsModel.find_by_id(id)
        if not dispatch_medications:
            return {'message': _("DISPATCH_MEDICATIONS_NOT_FOUND")}, 404

        try:
            with db.session.no_autoflush:
                # Se obtiene el depósito stock (de salida)
                deposit_stock = DepositStockModel.find_by_id(id=dispatch_medications.deposit_stock_id)

                # Se obtiene el stock
                stock = StockModel.query.filter_by(medicine_id=dispatch_medications.medicine_id).first()
                medicine_label = f"{stock.medicine.code} - {stock.medicine.description}"

                # Se obtiene los datos del paciente
                patient = PatientModel.query.filter_by(id=dispatch_medications.patient_id).first()
                patient_label = f"{patient.document_number} - {patient.firstname} {patient.lastname}"

                # Se resta la existencia del stock
                deposit_stock.quantity += dispatch_medications.quantity
                stock.quantity += dispatch_medications.quantity

                # Se registra en el historial
                historial = HistoryModel()
                historial.orig_deposit_stock = deposit_stock
                historial.quantity = +dispatch_medications.quantity
                historial.event_id = HistoryModel.get_event(EventCode.DISPENSE_REVERT)
                historial.description = f"Revert dispense of medicine {medicine_label} to patient {patient_label}"
                historial.user_create = get_jwt_identity()
                # historial.num_lot = dispatch_medications.num_lot
                db.session.add(historial)

                db.session.delete(dispatch_medications)
                db.session.commit()
        except Exception as error:
            # Se revierte los cambios
            db.session.rollback()
            msg = 'An error occurred while creating dispatch medications.'
            logging.error(f"{msg}. Details: {error.__cause__}", exc_info=error)
            return {"message": f"{msg}. Details: {error.__cause__}"}, 500

        return {'message': _("DISPATCH_MEDICATIONS_DELETED")}


class DispatchMedicationsList(Resource):

    @jwt_required()
    @check('dispatch_medications_list')
    @swag_from('../swagger/dispatch_medications/list_dispatch_medications.yaml')
    def get(self):
        query = DispatchMedicationsModel.query
        return paginated_results(query)

    @jwt_required()
    @check('dispatch_medications_insert')
    @swag_from('../swagger/dispatch_medications/post_dispatch_medications.yaml')
    def post(self):
        data = DispatchMedications.parser.parse_args()

        id = data.get('id')

        if id is not None and DispatchMedicationsModel.find_by_id(id):
            return {'message': _("DISPATCH_MEDICATIONS_DUPLICATED").format(id)}, 400

        dispatch_medications = DispatchMedicationsModel(**data)
        dispatch_medications.date_create = datetime.now()
        dispatch_medications.user_create = get_jwt_identity()
        try:
            with db.session.no_autoflush:
                # Se obtiene el depósito stock (de salida)
                deposit_stock = DepositStockModel.find_by_id(id=dispatch_medications.deposit_stock_id)

                # Se obtiene el stock
                stock = StockModel.query.filter_by(medicine_id=dispatch_medications.medicine_id).first()
                medicine_label = f"{stock.medicine.code} - {stock.medicine.description}"

                # Obtener el deposit_lot si existe
                deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposit_stock.id, lote_id=dispatch_medications.lote_id,
                                                              medicine_id=dispatch_medications.medicine_id).first()

                # Se obtiene los datos del paciente
                patient = PatientModel.query.filter_by(id=dispatch_medications.patient_id).first()
                patient_label = ''
                if patient:
                    patient_data = patient.json()
                    patient_label = f"{patient_data['document_number']} - {patient_data['firstname']} {patient_data['lastname']}"

                # Se resta la existencia del stock
                deposit_stock.quantity -= dispatch_medications.quantity
                stock.quantity -= dispatch_medications.quantity
                deposit_lot.quantity -= dispatch_medications.quantity

                num_lot = LotModel.query.filter_by(id=dispatch_medications.lote_id).first()
                # Se registra en el historial
                historial = HistoryModel()
                historial.orig_deposit_stock = deposit_stock
                historial.quantity = -dispatch_medications.quantity
                historial.event_id = HistoryModel.get_event(EventCode.DISPENSE_PAT)
                historial.description = f"Dispense of medicine {medicine_label} to patient {patient_label}"
                historial.user_create = get_jwt_identity()
                historial.num_lot = num_lot.num_lot
                db.session.add(historial)

                db.session.add(dispatch_medications)
                db.session.commit()
        except Exception as error:
            # Se revierte los cambios
            db.session.rollback()
            msg = 'An error occurred while creating dispatch medications.'
            logging.error(f"{msg}. Details: {error.__cause__}", exc_info=error)
            return {"message": f"{msg}. Details: {error.__cause__}"}, 500

        return dispatch_medications.json(), 201


class DispatchMedicationsSearch(Resource):

    @jwt_required()
    @check('dispatch_medications_search')
    @swag_from('../swagger/dispatch_medications/search_dispatch_medications.yaml')
    def post(self):
        key = current_app.config['ENCRYPTION_KEY']
        query = DispatchMedicationsModel.query
        query = query.join(PatientModel, and_(DispatchMedicationsModel.patient_id == PatientModel.id), isouter=True)
        query = query.join(MedicineModel, and_(DispatchMedicationsModel.medicine_id == MedicineModel.id), isouter=True)
        query = query.join(DepositStockModel, and_(DispatchMedicationsModel.deposit_stock_id == DepositStockModel.id), isouter=True)
        query = query.join(DepositModel, and_(DepositStockModel.deposit_id == DepositModel.id), isouter=True)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: DispatchMedicationsModel.id == x)
            or_filter_list = restrict(or_filter_list, filters, 'patient_id', lambda x: DispatchMedicationsModel.patient_id == x)  # Para busqueda por paciente no se utiliza or
            or_filter_list = restrict_collector(or_filter_list, filters, 'quantity', lambda x: cast(DispatchMedicationsModel.quantity, sqlalchemy.String) == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'date', lambda x: func.to_char(DispatchMedicationsModel.date, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'num_lot', lambda x: func.lower(
                DispatchMedicationsModel.num_lot).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'origin', lambda x: func.lower(DispatchMedicationsModel.origin).contains(func.lower(x)))

            # Relationship Filter
            or_filter_list = restrict_collector(or_filter_list, filters, 'patient', lambda x: func.lower(
                func.regexp_replace(func.decrypt_data(PatientModel.document_number, key) + " - " + func.decrypt_data(PatientModel.firstname, key) + " " + func.decrypt_data(PatientModel.lastname, key), '\s+', ' ', 'g')
            ).contains(func.lower(x.strip())))
            or_filter_list = restrict_collector(or_filter_list, filters, 'medicine', lambda x: func.lower(
                MedicineModel.code + " - " + MedicineModel.description
            ).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'deposit_stock', lambda x: func.lower(
                DepositModel.code + " - " + DepositModel.name
            ).contains(func.lower(x)))

            # query = apply_filters(query, filter_list)
        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
        return paginated_results(query)
