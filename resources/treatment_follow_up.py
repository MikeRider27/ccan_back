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
from models.dispatch_medications import DispatchMedicationsModel
from models.doctor import DoctorModel
from models.history import HistoryModel, EventCode
from models.lot import LotModel
from models.medicine_treatment_follow_up import MedicineTreatmentFollowUpModel
from models.parameter import ParameterModel
from models.patient import PatientModel, OriginsCode
from models.stock import StockModel
from models.treatment_follow_up import TreatmentFollowUpModel
from models.treatment_plan import TreatmentPlanModel
from security import check
from utils import restrict, paginated_results


def clean_medicine_tratment_follow_up(medicine_treatment_follow_up):
    if 'deposit_stock' in medicine_treatment_follow_up:
        del medicine_treatment_follow_up['deposit_stock']
    if 'medicine' in medicine_treatment_follow_up:
        del medicine_treatment_follow_up['medicine']
    if 'treatment_follow_up' in medicine_treatment_follow_up:
        del medicine_treatment_follow_up['treatment_follow_up']
    if 'deposit_id' in medicine_treatment_follow_up:
        del medicine_treatment_follow_up['deposit_id']


def add_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up,treatment_follow_up):

    stock = StockModel.query.filter_by(medicine_id=medicine_treatment_follow_up.medicine_id).first()
    # Se obtiene los datos del paciente
    patient = PatientModel.query.filter_by(id=treatment_follow_up.patient_id).first()
    patient_label = ''
    if patient:
        patient_data = patient.json()
        patient_label = f"{patient_data['document_number']} - {patient_data['firstname']} {patient_data['lastname']}"

    if stock is not None:
        deposit_stock = DepositStockModel.find_by_id(medicine_treatment_follow_up.deposit_stock_id)
        deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposit_stock.id,
                                                      medicine_id=medicine_treatment_follow_up.medicine_id).first()

        if deposit_stock is not None and deposit_lot is not None:
            final_quantity = deposit_stock.quantity - medicine_treatment_follow_up.quantity
            medicine_label = f"{stock.medicine.code} - {stock.medicine.description}"
            if final_quantity > 0:
                deposit_stock.quantity = deposit_stock.quantity - medicine_treatment_follow_up.quantity
                stock.quantity = stock.quantity - medicine_treatment_follow_up.quantity
                deposit_lot.quantity = deposit_lot.quantity - medicine_treatment_follow_up.quantity
                db.session.add(stock)
                db.session.add(deposit_stock)
                db.session.add(deposit_lot)

                #Se registra la entrega de medicamento
                # dispatch_medications_model = DispatchMedicationsModel()
                # dispatch_medications_model.deposit_stock_id = deposit_stock.id
                # dispatch_medications_model.patient_id = treatment_follow_up.patient_id
                # dispatch_medications_model.medicine_id = medicine_treatment_follow_up.medicine_id
                # dispatch_medications_model.quantity = deposit_stock.quantity
                # dispatch_medications_model.origin = OriginsCode.CCAN_CITY_SOFT.value
                # dispatch_medications_model.user_create = get_jwt_identity()
                # dispatch_medications_model.date = datetime.now()
                # dispatch_medications_model.lote_id = deposit_lot.lote_id
                # db.session.add(dispatch_medications_model)

                num_lot = LotModel.query.filter_by(id=deposit_lot.lote_id).first()

                historial = HistoryModel()
                historial.orig_deposit_stock = deposit_stock
                historial.quantity = -medicine_treatment_follow_up.quantity
                historial.event_id = HistoryModel.get_event(EventCode.REMOVE_BY_MEDICINE_TREATMENT_FOLLOW_UP)
                historial.description = f"Dispense of medicine {medicine_label} to patient {patient_label}"
                historial.user_create = get_jwt_identity()
                historial.num_lot = num_lot.num_lot
                db.session.add(historial)
            else:
                logging.error('Medicine Treatment Follow-up cannot be assigned because the final quantity is less than 0')
        else:
            logging.error('Deposit_stock does not exist')
    else:
        logging.error('The stock of the medicine cannot be found')


def delete_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up, treatment_follow_up):
    # TODO: tener en cuenta el estado del medicamento y del stock
    # Se obtiene el stock del medicamento
    stock = StockModel.query.filter_by(medicine_id=medicine_treatment_follow_up.medicine_id).first()
    medicine_label = ''
    if stock:
        medicine_label = f"{stock.medicine.code} - {stock.medicine.description}"
    # Se obtiene los datos del paciente
    patient = PatientModel.query.filter_by(id=treatment_follow_up.patient_id).first()
    patient_label = ''
    if patient:
        patient_data = patient.json()
        patient_label = f"{patient_data['document_number']} - {patient_data['firstname']} {patient_data['lastname']}"
    # Se obtiene el deposito stock
    deposito_stock = None
    if stock:
        deposito_stock = DepositStockModel.find_by_id(medicine_treatment_follow_up.deposit_stock_id)
        stock.quantity += medicine_treatment_follow_up.quantity
        db.session.add(stock)
    else:
        stock_state = ParameterModel.query.filter_by(domain='STOCK_STATE', code='A').first()
        stock = StockModel(id=None, medicine_id=medicine_treatment_follow_up.medicine_id,
                           quantity=medicine_treatment_follow_up.quantity,
                           state_id=stock_state.id)
        db.session.add(stock)
        db.session.flush()

    # Se actualiza el depósito stock
    if deposito_stock:
        deposito_stock.quantity += medicine_treatment_follow_up.quantity
    else:
        deposito_stock = DepositStockModel(id=None, deposit_id=medicine_treatment_follow_up.deposit_stock_id,
                                           stock_id=stock.id, quantity=medicine_treatment_follow_up.quantity)
    db.session.add(deposito_stock)

    deposit_lot = DepositLotModel.query.filter_by(deposit_stock_id=deposito_stock.id,
                                                  medicine_id=medicine_treatment_follow_up.medicine_id).first()
    if deposit_lot:
        deposit_lot.quantity += medicine_treatment_follow_up.quantity
        db.session.add(deposit_lot)

    # dispatch_medications_model = DispatchMedicationsModel.query.filter_by(
    #     deposit_stock_id=deposito_stock.id,
    #     patient_id=treatment_follow_up.patient_id,
    #     medicine_id=medicine_treatment_follow_up.medicine_id,
    #     lote_id=deposit_lot.lote_id).first()
    # if dispatch_medications_model:
    #     dispatch_medications_model.quantity += medicine_treatment_follow_up.quantity

    num_lot = LotModel.query.filter_by(id=deposit_lot.lote_id).first()

    historial = HistoryModel()
    historial.orig_deposit_stock = deposito_stock
    historial.quantity = -medicine_treatment_follow_up.quantity
    historial.event_id = HistoryModel.get_event(EventCode.ADD_BY_MEDICINE_TREATMENT_FOLLOW_UP)
    historial.description = f"Delete a dispense of medicine {medicine_label} to patient {patient_label}"
    historial.user_create = get_jwt_identity()
    historial.num_lot = num_lot.num_lot
    db.session.add(historial)


def update_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up_new, medicine_treatment_follow_up_old,treatment_follow_up):
    # Verificar si ha cambiado la medicina, el deposito o la cantidad
    change = False
    if medicine_treatment_follow_up_new.medicine_id != medicine_treatment_follow_up_old.medicine_id:
        change = True
    if medicine_treatment_follow_up_new.deposit_stock_id != medicine_treatment_follow_up_old.deposit_stock_id:
        change = True
    if medicine_treatment_follow_up_new.quantity != medicine_treatment_follow_up_old.quantity:
        change = True

    if change:
        delete_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up_new,treatment_follow_up)
        add_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up_old,treatment_follow_up)


class TreatmentFollowUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('follow_up_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('last_cancer_control_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('type_treatment', type=str)
    parser.add_argument('breast', type=str)
    parser.add_argument('armpit', type=bool)
    parser.add_argument('suspension_treatment', type=bool)
    parser.add_argument('suspension_treatment_reason', type=str)
    parser.add_argument('suspension_treatment_custom_reason', type=str)
    parser.add_argument('congestive_heart_failure', type=bool)
    parser.add_argument('fevi_follow_up_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('fevi_value', type=int)
    parser.add_argument('fevi_trastuzumab_dose', type=int)
    parser.add_argument('other_severe_adverse_events', type=bool)
    parser.add_argument('other_severe_adverse_events_detail', type=str)
    parser.add_argument('other_complementary_studies', type=str)
    parser.add_argument('dose_adjustment', type=bool)
    parser.add_argument('dose_adjustment_reason', type=str)
    parser.add_argument('comentaries', type=str)
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('medicine_list', type=list, location='json')
    parser.add_argument('treatment_plan_list', type=list, location='json')

    @jwt_required()
    @check('treatment_follow_up_get')
    @swag_from('../swagger/treatment_follow_up/get_treatment_follow_up.yaml')
    def get(self, id):
        treatment_follow_up = TreatmentFollowUpModel.find_by_id(id)
        if treatment_follow_up:
            return treatment_follow_up.json()
        return {'message': _("TREATMENT_FOLLOW_UP_NOT_FOUND")}, 404

    @jwt_required()
    @check('treatment_follow_up_update')
    @swag_from('../swagger/treatment_follow_up/put_treatment_follow_up.yaml')
    def put(self, id):
        treatment_follow_up = TreatmentFollowUpModel.find_by_id(id)
        if treatment_follow_up:
            newdata = TreatmentFollowUp.parser.parse_args()
            medicine_treatment_follow_up_data_list = newdata['medicine_list'] if newdata[
                                                                                     'medicine_list'] is not None else []
            del newdata['medicine_list']
            TreatmentFollowUpModel.from_reqparse(treatment_follow_up, newdata)
            medicine_treatment_follow_up_id_old = [medicine_treatment_follow_up.id for medicine_treatment_follow_up in
                                                   treatment_follow_up.medicine_list]
            medicine_treatment_follow_up_id_new = [medicine_treatment_follow_up['id'] for medicine_treatment_follow_up
                                                   in medicine_treatment_follow_up_data_list if
                                                   'id' in medicine_treatment_follow_up]
            medicine_treatment_follow_up_id_delete = list(
                set(medicine_treatment_follow_up_id_old) - set(medicine_treatment_follow_up_id_new))
            medicine_treatment_follow_up_id_update = list(
                set(medicine_treatment_follow_up_id_new) - set(medicine_treatment_follow_up_id_delete))
            medicine_treatment_follow_up_delete_list = [medicine_treatment_follow_up for medicine_treatment_follow_up in
                                                        treatment_follow_up.medicine_list if
                                                        medicine_treatment_follow_up.id in medicine_treatment_follow_up_id_delete]
            medicine_treatment_follow_up_update_list_old = [medicine_treatment_follow_up for
                                                            medicine_treatment_follow_up in
                                                            treatment_follow_up.medicine_list if
                                                            medicine_treatment_follow_up.id in medicine_treatment_follow_up_id_update]
            medicine_treatment_follow_up_update_list_new = [medicine_treatment_follow_up for
                                                            medicine_treatment_follow_up in
                                                            medicine_treatment_follow_up_data_list if
                                                            'id' in medicine_treatment_follow_up and
                                                            medicine_treatment_follow_up[
                                                                'id'] in medicine_treatment_follow_up_id_update]
            medicine_treatment_follow_up_add_list = [medicine_treatment_follow_up for medicine_treatment_follow_up in
                                                     medicine_treatment_follow_up_data_list if
                                                     'id' not in medicine_treatment_follow_up or
                                                     medicine_treatment_follow_up['id'] is None]

            follow_up_treatment_plan_data_list = newdata['treatment_plan_list']
            TreatmentFollowUpModel.from_reqparse(treatment_follow_up, newdata)

            try:
                with db.session.no_autoflush:
                    # medicine_treatment_follow_up update
                    medicine_treatment_follow_up_list = []

                    for new_medicine_treatment_follow_up in medicine_treatment_follow_up_add_list:
                        clean_medicine_tratment_follow_up(new_medicine_treatment_follow_up)
                        medicine_treatment_follow_up = MedicineTreatmentFollowUpModel(
                            **new_medicine_treatment_follow_up)

                        medicine_treatment_follow_up_list.append(medicine_treatment_follow_up)
                        # Se actualiza el stock vía el detalle
                        add_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up)
                        # add_lot_entries(lot_detail_model, lot)

                        # Delete
                    for delete_medicine_treatment_follow_up in medicine_treatment_follow_up_delete_list:
                        delete_medicine_treatment_follow_up_to_stock(delete_medicine_treatment_follow_up,treatment_follow_up)
                        db.session.delete(delete_medicine_treatment_follow_up)

                        # Update
                    for medicine_treatment_follow_up_old in medicine_treatment_follow_up_update_list_old:
                        # Obtener el elemento nuevo para comparar con el anterior
                        medicine_treatment_follow_up_new_dict = next(
                            x for x in medicine_treatment_follow_up_update_list_new if
                            x['id'] == medicine_treatment_follow_up_old.id)
                        clean_medicine_tratment_follow_up(medicine_treatment_follow_up_new_dict)
                        medicine_treatment_follow_up_new = MedicineTreatmentFollowUpModel(
                            **medicine_treatment_follow_up_new_dict)

                        # Se Ajusta Stock
                        update_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up_new, medicine_treatment_follow_up_old, treatment_follow_up)

                        # Cambios del Lot Detail
                        medicine_treatment_follow_up_old.medicine_id = medicine_treatment_follow_up_new.medicine_id
                        medicine_treatment_follow_up_old.quantity = medicine_treatment_follow_up_new.quantity
                        medicine_treatment_follow_up_old.deposit_stock_id = medicine_treatment_follow_up_new.deposit_stock_id
                        medicine_treatment_follow_up_old.observation = medicine_treatment_follow_up_new.observation
                        medicine_treatment_follow_up_old.dose = medicine_treatment_follow_up_new.dose
                        medicine_treatment_follow_up_old.presentation = medicine_treatment_follow_up_new.presentation
                        medicine_treatment_follow_up_old.concentration = medicine_treatment_follow_up_new.concentration

                        # Se persiste el detalle del lote
                        medicine_treatment_follow_up_list.append(medicine_treatment_follow_up_old)
                    # for medicine_treatment_follow_up_data in medicine_treatment_follow_up_data_list:
                    #     if medicine_treatment_follow_up_data.get('id', None):
                    #         medicine_treatment_follow_up_model = MedicineTreatmentFollowUpModel.find_by_id(medicine_treatment_follow_up_data['id'])
                    #         MedicineTreatmentFollowUpModel.from_reqparse(medicine_treatment_follow_up_model, medicine_treatment_follow_up_data)
                    #     else:
                    #         medicine_treatment_follow_up_model = MedicineTreatmentFollowUpModel(**medicine_treatment_follow_up_data)
                    #     medicine_treatment_follow_up_list.append(medicine_treatment_follow_up_model)
                    treatment_follow_up.medicine_list = medicine_treatment_follow_up_list

                    # treatment_plan_list update
                    follow_up_treatment_plan_list = []
                    for follow_up_treatment_plan_data in follow_up_treatment_plan_data_list:
                        id = follow_up_treatment_plan_data.get('treatment_plan_id', None)
                        treatment_plan_model = TreatmentPlanModel.find_by_id(id)
                        follow_up_treatment_plan_list.append(treatment_plan_model)
                    treatment_follow_up.treatment_plan_list = follow_up_treatment_plan_list

                    treatment_follow_up.user_modify = get_jwt_identity()
                    treatment_follow_up.date_modify = datetime.now()

                    # Se persisiten todos los cambios
                    db.session.add(treatment_follow_up)
                    db.session.commit()
                    return treatment_follow_up.json()
            except Exception as error:
                # Se revierte los cambios
                db.session.rollback()
                msg = "An error occurred while updating the Treatment follow up."
                logging.error(msg, exc_info=error)
                return {"message": msg}, 500
        return {'message': '_("TREATMENT_FOLLOW_UP_NOT_FOUND")'}, 404

    @jwt_required()
    @check('treatment_follow_up_delete')
    @swag_from('../swagger/treatment_follow_up/delete_treatment_follow_up.yaml')
    def delete(self, id):
        treatment_follow_up = TreatmentFollowUpModel.find_by_id(id)
        if treatment_follow_up:
            treatment_follow_up.delete_from_db()

        return {'message': _("TREATMENT_FOLLOW_UP_DELETED")}


class TreatmentFollowUpList(Resource):

    @jwt_required()
    @check('treatment_follow_up_list')
    @swag_from('../swagger/treatment_follow_up/list_treatment_follow_up.yaml')
    def get(self):
        query = TreatmentFollowUpModel.query
        return paginated_results(query)

    @jwt_required()
    @check('treatment_follow_up_insert')
    @swag_from('../swagger/treatment_follow_up/post_treatment_follow_up.yaml')
    def post(self):
        data = TreatmentFollowUp.parser.parse_args()

        id = data.get('id')

        if id is not None and TreatmentFollowUpModel.find_by_id(id):
            return {'message': _("TREATMENT_FOLLOW_UP_DUPLICATED").format(id)}, 400

        try:
            with db.session.no_autoflush:
                # medicine_list
                medicine_treatment_follow_up_data_list = data['medicine_list']
                del data['medicine_list']

                # treatment_plan_list
                follow_up_treatment_plan_data_list = data['treatment_plan_list']
                del data['treatment_plan_list']

                treatment_follow_up = TreatmentFollowUpModel(**data)

                # medicine_list process
                for medicine_treatment_follow_up_data in medicine_treatment_follow_up_data_list:
                    clean_medicine_tratment_follow_up(medicine_treatment_follow_up_data)
                    medicine_treatment_follow_up_model = MedicineTreatmentFollowUpModel(
                        **medicine_treatment_follow_up_data)
                    treatment_follow_up.medicine_list.append(medicine_treatment_follow_up_model)

                    # Se actualiza el stock vía el detalle
                    add_medicine_treatment_follow_up_to_stock(medicine_treatment_follow_up_model, treatment_follow_up)

                # treatment_plan_list
                for follow_up_treatment_plan_data in follow_up_treatment_plan_data_list:
                    id = follow_up_treatment_plan_data.get('treatment_plan_id', None)
                    treatment_plan_model = TreatmentPlanModel.find_by_id(id)
                    treatment_follow_up.treatment_plan_list.append(treatment_plan_model)

                # Se persisiten todos los cambios
                db.session.add(treatment_follow_up)
                db.session.commit()

        except Exception as error:
            # Se revierte los cambios
            db.session.rollback()
            msg = "An error occurred while creating the Treatment follow up."
            logging.error(msg, exc_info=error)
            return {"message": msg}, 500

        return treatment_follow_up.json(), 201


class TreatmentFollowUpSearch(Resource):

    @jwt_required()
    @check('treatment_follow_up_search')
    @swag_from('../swagger/treatment_follow_up/search_treatment_follow_up.yaml')
    def post(self):
        query = TreatmentFollowUpModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: TreatmentFollowUpModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: TreatmentFollowUpModel.patient_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: TreatmentFollowUpModel.hospital_id == x)
            query = restrict(query, filters, 'type_treatment',
                             lambda x: TreatmentFollowUpModel.type_treatment.contains(x))
            query = restrict(query, filters, 'breast', lambda x: TreatmentFollowUpModel.breast.contains(x))
            query = restrict(query, filters, 'armpit', lambda x: x)
            query = restrict(query, filters, 'suspension_treatment', lambda x: x)
            query = restrict(query, filters, 'suspension_treatment_reason',
                             lambda x: TreatmentFollowUpModel.suspension_treatment_reason.contains(x))
            query = restrict(query, filters, 'suspension_treatment_custom_reason',
                             lambda x: TreatmentFollowUpModel.suspension_treatment_custom_reason.contains(x))
            query = restrict(query, filters, 'congestive_heart_failure', lambda x: x)
            query = restrict(query, filters, 'fevi_value', lambda x: TreatmentFollowUpModel.fevi_value == x)
            query = restrict(query, filters, 'fevi_trastuzumab_dose',
                             lambda x: TreatmentFollowUpModel.fevi_trastuzumab_dose == x)
            query = restrict(query, filters, 'other_severe_adverse_events', lambda x: x)
            query = restrict(query, filters, 'other_severe_adverse_events_detail',
                             lambda x: TreatmentFollowUpModel.other_severe_adverse_events_detail.contains(x))
            query = restrict(query, filters, 'other_complementary_studies',
                             lambda x: TreatmentFollowUpModel.other_complementary_studies.contains(x))
            query = restrict(query, filters, 'dose_adjustment', lambda x: x)
            query = restrict(query, filters, 'dose_adjustment_reason',
                             lambda x: TreatmentFollowUpModel.dose_adjustment_reason.contains(x))
            query = restrict(query, filters, 'comentaries', lambda x: TreatmentFollowUpModel.comentaries.contains(x))
            query = restrict(query, filters, 'doctor_id', lambda x: DoctorModel.doctor_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(TreatmentFollowUpModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: TreatmentFollowUpModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(TreatmentFollowUpModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: TreatmentFollowUpModel.user_modify.contains(x))

        # default order
        query = query.order_by(TreatmentFollowUpModel.id.desc())

        return paginated_results(query)
