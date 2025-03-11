import datetime
import logging
import re

from datetime import datetime, timedelta
from flask import current_app
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy import func
from flask_babel import _

from dao.interoperabilidad_dao import InteroperabilidadDao
from dao.patient_dao import PatientDao
from db import db
from models.area import AreaModel
from models.cie_10 import Cie_10Model
from models.cie_o_morphology import CieOMorphologyModel
from models.cie_o_topography import CieOTopographyModel
from models.cie_o_tumor_location import CieOTumorLocationModel
from models.city import CityModel
from models.configuration import ConfigurationModel
from models.country import CountryModel
from models.deposit import DepositModel
from models.deposit_lot import DepositLotModel
from models.deposit_movement import DepositMovementModel
from models.deposit_stock import DepositStockModel
from models.diagnosis_ap import DiagnosisApModel
from models.dispatch_medications import DispatchMedicationsModel
from models.doctor import DoctorModel
from models.doctor_specialty import DoctorSpecialtyModel
from models.document_type import DocumentTypeModel
from models.entries import EntriesModel
from models.entries_deposit_stock import EntriesDepositStockModel
from models.entries_lot import EntriesLotModel
from models.gender import GenderModel
from models.history import HistoryModel, EventCode
from models.hospital import HospitalModel
from models.lot import LotModel
from models.medical_consultation import MedicalConsultationModel
from models.medicine import MedicineModel
from models.medicine_medical_consultation import MedicineMedicalConsultationModel
from models.parameter import ParameterModel
from models.patient import PatientModel, OriginsCode
from models.patient_hospital import PatientHospitalModel
from models.specialty import SpecialtyModel
from models.stock import StockModel
from utils import log_interoperability


def sync_patient_diagnosis_ap_sigap(patient_id):
    patient = PatientModel.find_by_id(patient_id)
    if not patient:
        return {'message': _("PATIENT_NOT_FOUND")}, 404

    # Get user via manual o automatic task
    try:
        user_create = get_jwt_identity()
    except:
        user_create = 'Interoperabilidad'

    patient_data = patient.json()
    patient_document = patient_data['document_number']
    interoperabilidad_dao = InteroperabilidadDao()
    interoperabilidad_data = interoperabilidad_dao.patient_data(patient_document=patient_document)

    try:
        with db.session.no_autoflush:
            for biopsia in interoperabilidad_data:
                fecha_informe = biopsia['fecha_informe']
                diagnosis_ap_object = DiagnosisApModel.query.filter_by(patient_id=patient_id,
                                                                       date=fecha_informe).first()
                # Si el registro ya no fue insertado anteriormente
                if not diagnosis_ap_object:
                    diagnosis_ap = DiagnosisApModel()
                else:
                    diagnosis_ap = diagnosis_ap_object

                # Mapeo hospital interoperabilidad con ccan
                map_hospital_list = interoperabilidad_dao.hospital_map()
                inter_hosp_id = biopsia['idestablecimiento']
                map_hospital = list(
                    filter(lambda x: x['interoperabilidad_id'] == inter_hosp_id, map_hospital_list)).pop()

                # Mapeo CIE-O morfologia interoperabilidad con readiness
                inter_cieo_morf_cod = biopsia['codigo_morfologia']
                map_cieo_morf = None
                if inter_cieo_morf_cod:
                    map_cieo_morf = CieOMorphologyModel.query.filter_by(code=inter_cieo_morf_cod).first()

                # Mapeo CIE-O topología interoperabilidad con readiness
                inter_cieo_topol_cod = biopsia['cod_topografia']
                map_cieo_topol = None
                if inter_cieo_topol_cod:
                    map_cieo_topol = CieOTopographyModel.query.filter_by(code=inter_cieo_topol_cod).first()

                # Mapeo CIE-O localización interoperabilidad con readiness
                inter_cieo_local_cod = biopsia['cod_localizacion']
                map_cieo_local = None
                if inter_cieo_local_cod:
                    map_cieo_local = CieOTumorLocationModel.query.filter_by(code=inter_cieo_local_cod).first()

                diagnosis_ap.patient_id = patient_id
                diagnosis_ap.date = fecha_informe
                diagnosis_ap.hospital_id = map_hospital.get('ccan_id', None)
                diagnosis_ap.cie_o_morphology_id = map_cieo_morf.id if map_cieo_morf else None
                diagnosis_ap.cie_o_topography_id = map_cieo_topol.id if map_cieo_topol else None
                diagnosis_ap.cie_o_tumor_location_id = map_cieo_local.id if map_cieo_local else None
                diagnosis_ap.armpit = 'no_data'
                diagnosis_ap.re = biopsia['re'].lower() if biopsia['re'] else None
                diagnosis_ap.rp = biopsia['rp'].lower() if biopsia['rp'] else None
                diagnosis_ap.her2 = biopsia['her2'].lower() if biopsia['her2'] else None
                diagnosis_ap.tumor_size = float(biopsia['tamanho_tumor']) if biopsia['tamanho_tumor'] else None
                diagnosis_ap.user_create = user_create
                diagnosis_ap.origin = OriginsCode.SIGAP.value

                # Campos de Reporte General
                diagnosis_ap.dx_presuntivo = biopsia['dx_presuntivo']
                diagnosis_ap.material = biopsia['material']
                diagnosis_ap.diagnostico = biopsia['diagnostico']
                diagnosis_ap.clasificacion = biopsia['clasificacion']
                diagnosis_ap.macroscopia = biopsia['macroscopia']
                diagnosis_ap.microscopia = biopsia['microscopia']
                db.session.add(diagnosis_ap)

                # Registro de log
                log_interoperability(operacion='Interoperar Diagnostigo AP (Biopsias) de Pacientes',
                                     origen=OriginsCode.SIGAP.value, data=biopsia)

            # Se confirman todos los cambios
            db.session.commit()
            return {'message': 'success'}, 200
    except Exception as err:
        # Se revierte los cambios
        db.session.rollback()

        msg = f"Ocurrió un error al registrar biopsia. detalle: {err.__cause__}"
        logging.error(msg, exc_info=err)
        return {"message": msg}, 500


class InteroperabilidadPatient(Resource):
    @jwt_required()
    # @check('interoperabilidad_patient_document')
    # @swag_from('../swagger/interoperabilidad/get_patient.yaml')
    def get(self, patient_id):
        config_active = ConfigurationModel.query.filter_by(code='IS', value='ACTIVE').first()
        if not config_active:
            return {'message': 'Los servicios de interoperabilidad no se encuentran activados'}, 400

        response, code = sync_patient_diagnosis_ap_sigap(patient_id)
        return response, code


def get_stock_movements(stock_id):
    stock: StockModel = StockModel.find_by_id(id=stock_id)
    medicine: MedicineModel = MedicineModel.find_by_id(id=stock.medicine_id)

    # Listado siciap
    history_list_siciap = []

    # SICIAP
    interoperabilidad_dao = InteroperabilidadDao()
    medicine_siciap_header_list = interoperabilidad_dao.get_medicine_history_siciap_header(codigo_medicamento=medicine.code)
    medicine_siciap_mov_list = interoperabilidad_dao.get_medicine_history_siciap(codigo_medicamento=medicine.code)
    for siciap_stock in medicine_siciap_mov_list:
        stock_data = {
            'origin': siciap_stock.get('origin'),
            'date': siciap_stock.get('date').strftime("%Y-%m-%dT%H:%M:%S.%f"),
            'description': siciap_stock.get('description'),
            'observation': siciap_stock.get('observation'),
            'origen_codigo': siciap_stock.get('origen_codigo'),
            'origen_tipo': siciap_stock.get('origen_tipo'),
            'origen_nombre': siciap_stock.get('origen_nombre'),
            'destino_codigo': siciap_stock.get('destino_codigo'),
            'destino_tipo': siciap_stock.get('destino_tipo'),
            'destino_nombre': siciap_stock.get('destino_nombre'),
            'quantity': siciap_stock.get('quantity'),  # cantidad
            'balance': siciap_stock.get('balance'),
            'codigo_medicamento': siciap_stock.get('codigo_medicamento'),  # codigo_medicamento
            'producto_nombre': siciap_stock.get('producto_nombre'),  # producto_nombre
            'producto_concentracion': siciap_stock.get('producto_concentracion'),  # producto_concentracion
            'producto_presentacion': siciap_stock.get('producto_presentacion'),  # producto_presentacion
            'producto_forma_farmaceutica': siciap_stock.get('producto_forma_farmaceutica'),
            # producto_forma_farmaceutica
            'fecha_vencimiento': siciap_stock.get('fecha_vencimiento'),  # fecha_vencimiento
            'numero_lote': siciap_stock.get('numero_lote'),
            'origen_interoperabilidad': OriginsCode.SICIAP.value,
        }
        history_list_siciap.append(stock_data)

    history_by_deposit_siciap = []
    # Group by deposit and lot
    for mov_dep_lot in medicine_siciap_header_list:
        codigo = mov_dep_lot.get('origen_codigo')
        dep = next((hist for hist in history_by_deposit_siciap if hist.get('deposit').get('codigo') == codigo), None)
        numero_lote = mov_dep_lot.get('numero_lote')
        lote_obj = {
            'numero_lote': numero_lote,
            'movements': sorted([mov for mov in history_list_siciap if mov.get('origen_codigo') == codigo and mov.get('numero_lote') == numero_lote], key=lambda x: x.get('date'))
        }
        if dep:
            dep['lot_list'].append(lote_obj)
        else:
            # Se agrega el depósito
            history_by_deposit_siciap.append({
                'deposit': {
                    'codigo': mov_dep_lot.get('origen_codigo'),
                    'tipo': mov_dep_lot.get('origen_tipo'),
                    'nombre': mov_dep_lot.get('origen_nombre')
                },
                'lot_list': [lote_obj]
            })

    # Ajuste de cantidad procesada
    for dep in history_by_deposit_siciap:
        for lote in dep.get('lot_list', []):
            balance = 0
            for mov in lote.get('movements', []):
                mov['quantity_procesed'] = mov.get('balance') - balance
                balance = mov['balance']

    # Datos del medicamento
    medicine_siciap = {}
    if len(medicine_siciap_mov_list) > 0:
        first_medicine_siciap = medicine_siciap_mov_list[0]
        medicine_siciap = {
            'codigo': first_medicine_siciap.get('codigo_medicamento'),  # codigo_medicamento
            'nombre': first_medicine_siciap.get('producto_nombre'),  # producto_nombre
            'concentracion': first_medicine_siciap.get('producto_concentracion'),  # producto_concentracion
            'presentacion': first_medicine_siciap.get('producto_presentacion'),  # producto_presentacion
            'forma_farmaceutica': first_medicine_siciap.get('producto_forma_farmaceutica'),
        }

    # CCAN
    # Listado siciap
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
    # SICIAP
    total_stock_siciap = 0
    for dep in history_by_deposit_siciap:
        dep['total'] = 0
        for lote in dep.get('lot_list', []):
            lote['total'] = 0
            if len(lote.get('movements', [])) > 0:
                last_mov = lote['movements'][-1]
                lote['total'] = last_mov.get('balance')
                dep['total'] += lote['total']
        total_stock_siciap += dep['total']

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
        'medicine': medicine_siciap,
        'siciap': {
            'total_stock': total_stock_siciap,
            'deposits': history_by_deposit_siciap
        },
        'ccan': {
            'total_stock': total_stock_ccan,
            'deposits': history_by_deposit_ccan
        }
    }

    return return_data


def sync_stock_movements_from_siciap(stock_id, data):
    try:
        # Get user via manual o automatic task
        try:
            user_create = get_jwt_identity()
        except:
            user_create = 'Interoperabilidad'

        with db.session.no_autoflush:
            # Se obtiene el stock del medicamento
            stock: StockModel = StockModel.query.filter_by(id=stock_id).first()

            # Se actualiza registro de medicamento desde interoperabilidad
            medicine_data = data.get('medicine', {})
            if medicine_data:
                medicine_model: MedicineModel = MedicineModel.query.filter_by(id=stock.medicine_id).first()
                if medicine_model:
                    medicine_model.generic_name = medicine_data.get('nombre').strip() if medicine_data.get(
                        'nombre') else None
                    medicine_model.concentration = medicine_data.get('concentracion').strip() if medicine_data.get(
                        'concentracion') else None
                    medicine_model.presentation = medicine_data.get('presentacion').strip() if medicine_data.get(
                        'presentacion') else None
                    medicine_model.pharmaceutical_form = medicine_data.get(
                        'forma_farmaceutica').strip() if medicine_data.get('forma_farmaceutica') else None
                    db.session.add(medicine_model)

            # Se prepara el stock de cada depósito para la sincronización.
            for deposit_stock in stock.deposit_stock_list:
                if deposit_stock.quantity > 0:
                    deposit_stock.quantity = 0
                    db.session.add(deposit_stock)

            # Se sincroniza los deposit_stock de CCAN con los valores de SICIAP
            siciap_data = data.get('siciap', {})
            siciap_depositos = siciap_data.get('deposits', [])
            for dep in siciap_depositos:
                deposit = dep.get('deposit', {})
                codigo_dep = str(deposit.get('codigo')) if deposit.get('codigo') else None
                tipo_dep = deposit.get('tipo')
                nombre_dep = deposit.get('nombre')
                total = dep.get('total')
                # Se verifica la existencia del depósito
                ccan_dep_model = DepositModel.query.filter_by(code=codigo_dep).first()
                if not ccan_dep_model:
                    # Se verifica la existencia del tipo de depósito
                    type_dep_model = ParameterModel.query.filter_by(domain='DEPOSIT_STOCK_TYPE',
                                                                    value=tipo_dep).first()
                    if not type_dep_model:
                        type_dep_model = ParameterModel()
                        type_dep_model.domain = 'DEPOSIT_STOCK_TYPE'
                        type_dep_model.value = tipo_dep
                        type_dep_model.active = True
                        type_dep_model.code = ''.join(word[0].upper() for word in tipo_dep.split())
                        db.session.add(type_dep_model)
                        db.session.flush()

                    ccan_dep_model = DepositModel()
                    ccan_dep_model.code = codigo_dep
                    ccan_dep_model.type = type_dep_model
                    ccan_dep_model.name = nombre_dep
                    ccan_dep_model.user_create = user_create
                    ccan_dep_model.origin = OriginsCode.SICIAP.value
                    db.session.add(ccan_dep_model)
                    db.session.flush()

                lote_list = dep.get('lot_list', [])
                movement_balance = 0
                for x in lote_list:
                    movement_lenght = len(x.get('movements', []))
                    movement = x.get('movements', [])
                    calculo_balance = int(movement[movement_lenght - 1].get('balance'))
                    movement_balance += calculo_balance

                for x in lote_list:
                    # Se verifica la existencia del deposit_stock
                    deposit_stock_model: DepositStockModel = DepositStockModel.query.filter_by(stock_id=stock_id,
                                                                                               deposit_id=ccan_dep_model.id).first()
                    if not deposit_stock_model:
                        deposit_stock_model = DepositStockModel()
                        deposit_stock_model.stock_id = stock_id
                        deposit_stock_model.deposit_id = ccan_dep_model.id
                        deposit_stock_model.quantity = 0

                    # Se ajusta la cantidad si hay cambios
                    if movement_balance > deposit_stock_model.quantity:
                        deposit_stock_model.quantity = movement_balance
                    db.session.add(deposit_stock_model)
                    db.session.flush()

                    # Obtener el lote por deposito
                    lote = x.get('numero_lote')
                    lot_model = LotModel.query.filter_by(num_lot=lote).first()
                    if not lot_model:
                        lot_model = LotModel()
                        lot_model.num_lot = lote
                        lot_model.date = None
                        lot_model.user_create = user_create
                        lot_model.origin = OriginsCode.SICIAP.value
                        db.session.add(lot_model)
                        db.session.flush()

                    # Se verifica la existencia de deposit_lot
                    deposit_lot_model: DepositLotModel = DepositLotModel.query.filter_by(deposit_stock_id=deposit_stock_model.id, medicine_id=medicine_model.id).first()

                    # Se crea el deposit_lot si no existe
                    if not deposit_lot_model:
                        deposit_lot_model = DepositLotModel()
                        deposit_lot_model.deposit_stock_id = deposit_stock_model.id
                        deposit_lot_model.lote_id = lot_model.id
                        deposit_lot_model.medicine_id = medicine_model.id
                        deposit_lot_model.quantity = 0
                    # Se ajusta la cantidad si hay cambios
                    if movement_balance > deposit_lot_model.quantity:
                        deposit_lot_model.quantity = movement_balance
                    db.session.add(deposit_lot_model)

            # Se registra movimientos en el historial de cambios
            # En este punto no se esperan nuevos depósitos para este stock
            for dep in siciap_depositos:
                for lot in dep.get('lot_list', []):
                    # Se obtiene el Lote
                    numero_lote_siciap = lot.get('numero_lote')
                    # Se obtiene los movimientos
                    movements = lot.get('movements')
                    for mov in movements:
                        lot_model: LotModel = None
                        if numero_lote_siciap:
                            lot_model = LotModel.query.filter_by(num_lot=numero_lote_siciap).first()
                            if not lot_model:
                                lot_model = LotModel()
                                lot_model.num_lot = numero_lote_siciap
                                lot_model.date = None
                                lot_model.user_create = user_create
                                lot_model.origin = OriginsCode.SICIAP.value
                                db.session.add(lot_model)
                                db.session.flush()

                        # Se obtiene el deposito origen
                        orig_deposit_stock_model = None
                        orig_dep_code = str(mov.get('origen_codigo')) if mov.get('origen_codigo') else None
                        if orig_dep_code:
                            orig_dep_model = DepositModel.query.filter_by(code=orig_dep_code).first()
                            if orig_dep_model:
                                orig_deposit_stock_model = DepositStockModel.query.filter_by(stock_id=stock_id,
                                                                                             deposit_id=orig_dep_model.id).first()

                        # Se obtiene el depósito destino
                        dest_deposit_stock_model = None
                        dest_dep_code = str(mov.get('destino_codigo')) if mov.get('destino_codigo') else None
                        if dest_dep_code:
                            dest_dep_model = DepositModel.query.filter_by(code=dest_dep_code).first()
                            if dest_dep_model:
                                dest_deposit_stock_model = DepositStockModel.query.filter_by(stock_id=stock_id,
                                                                                             deposit_id=dest_dep_model.id).first()

                        if orig_deposit_stock_model is not None and dest_deposit_stock_model is not None:
                            if orig_deposit_stock_model != dest_deposit_stock_model:
                                # Preparar la fecha para que la consulta pueda reconocerla
                                mov_date = datetime.strptime(mov.get('date'), '%Y-%m-%dT%H:%M:%S.%f')
                                mov_date = mov_date.replace(second=0, microsecond=0)
                                # Definir un rango de 1 minuto alrededor de la fecha
                                start_date = mov_date
                                end_date = mov_date + timedelta(minutes=1)

                                deposit_movement = DepositMovementModel.query.filter(
                                    DepositMovementModel.deposit_stock_in_id == orig_deposit_stock_model.id,
                                    DepositMovementModel.deposit_stock_out_id == dest_deposit_stock_model.id,
                                    DepositMovementModel.date_create >= start_date,
                                    DepositMovementModel.date_create < end_date,
                                    DepositMovementModel.lote_id == lot_model.id).first()

                                if not deposit_movement:
                                    if mov.get('quantity_procesed') > 0:
                                        deposit_movement = DepositMovementModel()
                                        deposit_movement.deposit_stock_in_id = orig_deposit_stock_model.id
                                        deposit_movement.deposit_stock_out_id = dest_deposit_stock_model.id
                                        deposit_movement.quantity = mov.get('quantity_procesed')
                                        deposit_movement.date_create = mov.get('date')
                                        deposit_movement.user_create = 'Interoperabilidad'
                                        deposit_movement.lote_id = lot_model.id
                                        db.session.add(deposit_movement)

                        # Se registra entrada
                        if lot_model:
                            mov_observation = mov.get('observation')
                            if mov_observation.strip() == 'ADQUISICIÓN DE MEDICAMENTOS':
                                # Se obtiene el registro entries_lot
                                entries_lot_model: EntriesLotModel = EntriesLotModel.query.filter_by(
                                    lot_id=lot_model.id).first()
                                if not entries_lot_model:
                                    # Se ajusta fecha del lote
                                    lot_model.date = mov.get('date')
                                    db.session.add(lot_model)

                                    # Se crea el entries
                                    entries_model = EntriesModel()
                                    entries_model.deposit_id = orig_dep_model.id
                                    entries_model.medicine_id = medicine_model.id
                                    entries_model.description = mov.get('description')
                                    entries_model.expiration_date = mov.get('fecha_vencimiento')
                                    entries_model.quantity = mov.get('quantity')
                                    entries_model.manufacturer_id = None
                                    entries_model.manufacturing_date = None
                                    entries_model.supplier_id = None
                                    entries_model.storage_conditions = None
                                    entries_model.observation = mov_observation
                                    entries_model.date = mov.get('date')
                                    entries_model.origin = OriginsCode.SICIAP.value
                                    entries_model.lote_id = lot_model.id
                                    db.session.add(entries_model)
                                    db.session.flush()

                                    # Se crea el entries_lot
                                    entries_lot_model = EntriesLotModel()
                                    entries_lot_model.lot_id = lot_model.id
                                    entries_lot_model.entries_id = entries_model.id
                                    db.session.add(entries_lot_model)

                                    # Se crea el entries_deposit_stock
                                    entries_deposit_stock_model = EntriesDepositStockModel()
                                    entries_deposit_stock_model.entries_id = entries_model.id
                                    entries_deposit_stock_model.deposit_stock_id = orig_deposit_stock_model.id
                                    db.session.add(entries_deposit_stock_model)

                        # Se verifica que el historial ya no haya sido migrado previamente
                        mov_date = mov.get('date')
                        mov_org_dep_id = orig_deposit_stock_model.id if orig_deposit_stock_model else None
                        mov_original_quantity = mov.get('quantity')
                        mov_description = mov.get('description')
                        mov_observation = mov.get('observation')
                        historial_model = HistoryModel.query.filter_by(date=mov_date,
                                                                       orig_deposit_stock_id=mov_org_dep_id,
                                                                       original_quantity=mov_original_quantity,
                                                                       description=mov_description,
                                                                       observation=mov_observation).first()
                        if not historial_model:
                            # Se registra en historial el movimiento
                            historial = HistoryModel()
                            historial.date = mov_date
                            historial.orig_deposit_stock = orig_deposit_stock_model
                            historial.dest_deposit_stock = dest_deposit_stock_model
                            historial.quantity = mov.get('quantity_procesed')
                            historial.event_id = HistoryModel.get_event(EventCode.SYNC_SICIAP)
                            historial.description = mov_description
                            historial.observation = mov_observation
                            historial.user_create = user_create
                            historial.origin = OriginsCode.SICIAP.value
                            historial.balance = mov.get('balance')
                            historial.original_quantity = mov_original_quantity
                            historial.num_lot = numero_lote_siciap
                            db.session.add(historial)

                            # Registro de log
                            log_interoperability(operacion='Interoperar Movimientos de Stock',
                                                 origen=OriginsCode.SICIAP.value, data=mov)

            # Se sincroniza el stock total de CCAN con el stock total de SICIAP
            stock.quantity = siciap_data.get('total_stock')
            db.session.add(stock)

            # Se confirman todos los cambios
            db.session.commit()
            return {'message': 'success'}, 200
    except Exception as error:
        # Se revierte los cambios
        db.session.rollback()

        logging.error(error, exc_info=error)
        return {"message": error.__cause__}, 500


class InteroperabilidadStock(Resource):
    @jwt_required()
    def get(self, stock_id):
        config_active = ConfigurationModel.query.filter_by(code='IS', value='ACTIVE').first()
        if not config_active:
            return {'message': 'Los servicios de interoperabilidad no se encuentran activados'}, 400

        return_data = get_stock_movements(stock_id)
        return return_data, 200

    @jwt_required()
    def post(self, stock_id):
        config_active = ConfigurationModel.query.filter_by(code='IS', value='ACTIVE').first()
        if not config_active:
            return {'message': 'Los servicios de interoperabilidad no se encuentran activados'}, 400

        data = request.json
        response, code = sync_stock_movements_from_siciap(stock_id, data)
        return response, code


def sync_patient_consultation_his(patient_id):
    patient = PatientModel.find_by_id(patient_id)
    if not patient:
        return {'message': 'No se encuentra Patient'}, 404

    # Obtener usuario manual o por tarea automática
    try:
        user_create = get_jwt_identity()
    except:
        user_create = 'Interoperabilidad'

    patient_data = patient.json()
    patient_document = patient_data['document_number']
    patient_registration_date = patient.registration_date
    interoperabilidad_dao = InteroperabilidadDao()
    interoperabilidad_data = interoperabilidad_dao.get_patient_consultation_his(
        patient_document=patient_document,
        patient_registration_date=patient_registration_date
    )

    try:
        with db.session.no_autoflush:
            for consultation_data in interoperabilidad_data:
                fecha_consulta = consultation_data['fecha']

                # Verificar si ya existe una consulta en la misma fecha y si proviene de HIS (HIS tiene prioridad sobre CCAN)
                existing_consultation = MedicalConsultationModel.query.filter_by(
                    patient_id=patient_id,
                    date_consultation=fecha_consulta,
                    origin='HIS'
                ).first()

                if existing_consultation:
                    consultation_model = existing_consultation
                else:
                    consultation_model = MedicalConsultationModel()
                    consultation_model.patient_id = patient_id
                    consultation_model.date_consultation = fecha_consulta
                    consultation_model.hospital_id = None
                    consultation_model.origin = OriginsCode.HIS.value
                    consultation_model.user_create = user_create

                    # Mapeo CIE-10 interoperabilidad con CCAN
                    inter_cie10_cod = consultation_data['cie_10_cm']
                    if re.match(r'^.*\.\d$', inter_cie10_cod):
                        inter_cie10_cod = inter_cie10_cod
                    else:
                        inter_cie10_cod = inter_cie10_cod.rstrip('.')

                    if inter_cie10_cod:
                        map_cie10 = Cie_10Model.query.filter_by(code=inter_cie10_cod).first()
                        consultation_model.cie_10_id = map_cie10.id if map_cie10 else None

                    # Obtener Hospital, de lo contrario crear
                    hospital = consultation_data.get('hospital_codigo')
                    if hospital:
                        hospital_model = HospitalModel.query.filter_by(hospital_codigo=hospital).first()
                        if not hospital_model:
                            hospital_model = HospitalModel()
                            hospital_model.description = consultation_data.get('Nombre')
                            hospital_model.country_id = 1
                            hospital_model.user_create = user_create
                            hospital_model.system = False
                            hospital_model.hospital_codigo = hospital
                            db.session.add(hospital_model)
                            db.session.flush()
                        consultation_model.hospital_id = hospital_model.id

                    # Obtener Doctor, de lo contrario crear
                    doctor_document = consultation_data.get('profesional_de_la_salud')
                    if doctor_document:
                        doctor_model = DoctorModel.query.filter_by(document_number=doctor_document).first()
                        if not doctor_model:
                            doctor_model = DoctorModel()
                            doctor_model.document_number = doctor_document
                            doctor_model.firstname = consultation_data.get('medico_nombres')
                            doctor_model.lastname = consultation_data.get('medico_apellidos')
                            doctor_model.user_create = user_create
                            doctor_model.origin = OriginsCode.HIS.value
                            db.session.add(doctor_model)
                            db.session.flush()
                        consultation_model.responsible_doctor_id = doctor_model.id

                        # Obtener especialidad del doctor, de lo contrario crear y asignar
                        doctor_specialty = consultation_data.get('especialidad')
                        if doctor_specialty:
                            specialty_model = SpecialtyModel.query.filter(
                                func.unaccent(func.lower(SpecialtyModel.description)).contains(
                                    func.unaccent(func.lower(doctor_specialty)))).first()
                            if not specialty_model:
                                specialty_model = SpecialtyModel()
                                specialty_model.description = doctor_specialty.upper()
                                specialty_model.origin = OriginsCode.HIS.value
                                db.session.add(specialty_model)
                                db.session.flush()

                            # Obtener relacion de especialidad con doctor
                            doctor_specialty_model = DoctorSpecialtyModel.query.filter_by(
                                doctor_id=doctor_model.id,
                                specialty_id=specialty_model.id).first()
                            if not doctor_specialty_model:
                                doctor_specialty_model = DoctorSpecialtyModel()
                                doctor_specialty_model.doctor_id = doctor_model.id
                                doctor_specialty_model.specialty_id = specialty_model.id
                                db.session.add(doctor_specialty_model)
                                db.session.flush()

                    observacion_list = []
                    tipo_consulta = consultation_data.get('tipo_de_consulta')
                    motivo_consulta = consultation_data.get('motivo_consulta')
                    if tipo_consulta:
                        observacion_list.append(f"Tipo de Consulta: {tipo_consulta}.")
                    if motivo_consulta:
                        observacion_list.append(f"Motivo de la consulta: {motivo_consulta}.")
                    consultation_model.observation = "\n".join(observacion_list)

                    db.session.add(consultation_model)
                    db.session.flush()  # Obtener id de la consulta

                # Obtener Medicina y agregarla a la consulta
                inter_medicine_cod = str(consultation_data.get('codigo_medicamento'))
                if inter_medicine_cod:
                    map_medicine = MedicineModel.query.filter_by(code=inter_medicine_cod).first()
                    if map_medicine:
                        # Verificar si la medicina ya está asociada a la consulta
                        existing_medicine_consultation = MedicineMedicalConsultationModel.query.filter_by(
                            medical_consultation_id=consultation_model.id,
                            medicine_id=map_medicine.id
                        ).first()

                        if not existing_medicine_consultation:
                            medicine_medical_consultation_model = MedicineMedicalConsultationModel()
                            medicine_medical_consultation_model.medical_consultation_id = consultation_model.id
                            medicine_medical_consultation_model.medicine_id = map_medicine.id
                            medicine_medical_consultation_model.presentation = consultation_data[
                                'descripcion_medicamento']
                            medicine_medical_consultation_model.quantity = consultation_data['cantidad_recetada']
                            medicine_medical_consultation_model.dose = consultation_data['cantidad_dispensada']
                            db.session.add(medicine_medical_consultation_model)

                # Registro de log
                log_interoperability(operacion='Interoperar Consultas de Pacientes', origen=OriginsCode.HIS.value,
                                     data=consultation_data)

            # Se confirman todos los cambios
            db.session.commit()
            return {'message': 'success'}, 200
    except Exception as err:
        # Se revierte los cambios
        db.session.rollback()

        msg = f"Ocurrió un error al registrar consulta médica. detalle: {err.__cause__}"
        logging.error(msg, exc_info=err)
        return {"message": msg}, 500


class InteroperabilidadPatientConsultation(Resource):
    @jwt_required()
    def get(self, patient_id):
        config_active = ConfigurationModel.query.filter_by(code='IS', value='ACTIVE').first()
        if not config_active:
            return {'message': 'Los servicios de interoperabilidad no se encuentran activados'}, 400

        response, code = sync_patient_consultation_his(patient_id)
        sync_patient_dispatch_medication_his(patient_id)
        return response, code


def sync_patient_sigap():
    config_active = ConfigurationModel.query.filter_by(code='IS', value='ACTIVE').first()
    if not config_active:
        return {'message': 'Los servicios de interoperabilidad no se encuentran activados'}, 400

    # Get user via manual o automatic task
    try:
        user_create = get_jwt_identity()
    except:
        user_create = 'Interoperabilidad'

    # SIGAP
    interoperabilidad_dao = InteroperabilidadDao()
    patient_list = interoperabilidad_dao.get_patients_sigap()

    try:
        with db.session.no_autoflush:
            cipher_key = current_app.config['ENCRYPTION_KEY']

            # Agregar o actualizar
            for patient_data in patient_list:
                # Verificación de duplicidad
                pat_tipo_documento = patient_data.get('tipo_documento')
                tipo_documento = DocumentTypeModel.query.filter_by(code=pat_tipo_documento).first()
                pat_documento_nro = patient_data.get('documento_nro')

                # Get Gender
                gender = GenderModel.query.filter_by(code=patient_data.get('sexo')).first()

                # Get City
                city = CityModel.query.filter(
                    func.lower(CityModel.description) == func.lower(patient_data.get('ciudad'))).first()

                # Get Area
                area = None
                if city:
                    area = AreaModel.query.filter(AreaModel.id == city.area_id).first()

                # Get Country
                country = None
                if area:
                    country = CountryModel.query.filter(CountryModel.id == area.country_id).first()

                # Get Civil Status
                civil_status = ParameterModel.query.filter_by(domain='PATIENT_CIVIL_STATUS',
                                                              code=patient_data.get('estado_civil')).first()

                # Get Patient State
                patient_state_sosp = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='SOSP').first()

                # Get Patient Vital State
                patient_vital_state_vivo = ParameterModel.query.filter_by(domain='PATIENT_VITAL_STATE',
                                                                          code='V').first()

                # Mapeo hospital interoperabilidad con ccan
                map_hospital_list = interoperabilidad_dao.hospital_map()
                inter_hosp_id = patient_data.get('id_establecimiento')
                map_hospital_filter = list(filter(lambda x: x['interoperabilidad_id'] == inter_hosp_id, map_hospital_list))
                map_hospital = map_hospital_filter.pop() if len(map_hospital_filter) > 0 else {}

                # Get Nacionality
                nacionality = CountryModel.query.filter(
                    CountryModel.nationality == patient_data.get('nacionalidad')).first()

                patient_model: PatientModel = PatientModel.query.filter(
                    PatientModel.document_type_id == tipo_documento.id,
                    func.decrypt_data(PatientModel.document_number, cipher_key) == pat_documento_nro).first()

                # Si aún no existe, agregar el paciente con datos iniciales
                if not patient_model:
                    patient_model: PatientModel = PatientModel()
                    patient_model.state_id = patient_state_sosp.id
                    patient_model.vital_state_id = patient_vital_state_vivo.id
                    patient_model.origin = OriginsCode.SIGAP.value if patient_data.get('origen_interoperabilidad') else OriginsCode.HIS.value
                    patient_model.user_create = user_create
                    patient_model.number_card = patient_data.get('nro_ficha')

                    if not patient_model.registration_date:
                        patient_model.registration_date = patient_data.get('fecha_creacion') if patient_data.get(
                            'fecha_creacion') else datetime.now()

                    # Relacionar paciente con hospital
                    hos_id = map_hospital.get('ccan_id', None)
                    if hos_id:
                        exist_hospital = list(filter(lambda x: x.hospital_id == hos_id, patient_model.hospital_list))
                        # Si el paciente no está relacionado con hospital, agregar relación
                        if len(exist_hospital) == 0:
                            pat_hos = PatientHospitalModel()
                            pat_hos.hospital_id = hos_id
                            patient_model.hospital_list.append(pat_hos)

                    # Si el hospital proviene de registros del HIS
                    hospital_codigo = patient_data.get('hospital_codigo')
                    if hospital_codigo:
                        # Obtener el hospital vía el código
                        hospital_model = HospitalModel.query.filter_by(hospital_codigo=hospital_codigo).first()
                        if hospital_model:
                            exist_hospital = list(
                                filter(lambda x: x.hospital_id == hospital_model.id, patient_model.hospital_list))
                            # Si el paciente no está relacionado con hospital, agregar relación
                            if len(exist_hospital) == 0:
                                pat_hos = PatientHospitalModel()
                                pat_hos.hospital_id = hospital_model.id
                                patient_model.hospital_list.append(pat_hos)

                patient_model.document_type_id = tipo_documento.id
                patient_model.document_number = pat_documento_nro
                patient_model.firstname = patient_data.get('nombres')
                patient_model.lastname = patient_data.get('apellidos')
                patient_model.birthdate = patient_data.get('fecha_nac') if patient_data.get('fecha_nac') else None
                patient_model.address = patient_data.get('direccion')
                patient_model.gender_id = gender.id if gender else None
                patient_model.city_id = city.id if city else None
                patient_model.area_id = area.id if area else None
                patient_model.country_id = country.id if country else None
                patient_model.phone = patient_data.get('telefono_1')
                patient_model.civil_status_id = civil_status.id if civil_status else None
                patient_model.nationality_id = nacionality.id if nacionality else None

                # Encript Data
                patient_model.encript_data()

                db.session.add(patient_model)
                db.session.flush()

                # Registro de log
                log_interoperability(operacion='Interoperar Pacientes con Cancer de Mama',
                                     origen=OriginsCode.SIGAP.value, data=patient_data)

                # Agregar diagnosis ap
                sync_patient_diagnosis_ap_sigap(patient_model.id)

                # Agregar diagnosis
                sync_patient_consultation_his(patient_model.id)

            # Se confirman todos los cambios
            db.session.commit()
            return {'message': 'success'}, 200
    except Exception as err:
        # Se revierte los cambios
        db.session.rollback()

        msg = f"Ocurrió un error al migrar pacientes desde el SIGAP. detalle: {err.__cause__}"
        logging.error(msg, exc_info=err)
        return {"message": msg}, 500


def sync_patient_dispatch_medication_siciap():
    config_active = ConfigurationModel.query.filter_by(code='IS', value='ACTIVE').first()
    if not config_active:
        return {'message': 'Los servicios de interoperabilidad no se encuentran activados'}, 400

    # Get user via manual o automatic task
    try:
        user_create = get_jwt_identity()
    except:
        user_create = 'Interoperabilidad'

    # Se obtiene los medicamentos en seguimiento
    medicine_list = MedicineModel.query.join(StockModel).filter(MedicineModel.stock_control == True).all()

    # Se obtiene la lista de pacientes
    patient_dao = PatientDao()
    patient_list = patient_dao.get_patients_document()

    # Dao
    interoperabilidad_dao = InteroperabilidadDao()

    try:
        with db.session.no_autoflush:
            # Se itera por cada medicamento
            for medicine in medicine_list:
                med_code = medicine.code
                for patient_data in patient_list:
                    patient_id = patient_data.get('patient_id')
                    patient_document_number = patient_data.get('patient_document_number')
                    patient_registration_date = patient_data.get('patient_registration_date')

                    # Se considera todos los consumos y no desde la fecha de creación del paciente
                    dispatch_medications_list = interoperabilidad_dao.get_patient_dispatch_medications(
                        medicine_code=med_code, patient_document=patient_document_number,
                        patient_registration_date=patient_registration_date)
                    for dispatch_medication in dispatch_medications_list:
                        # Get Deposit
                        codigo_dep = str(dispatch_medication.get('codigo_sucursal'))
                        # Verificar la posibilidad de crear el deposito si no existe
                        ccan_dep_model = DepositModel.query.filter_by(code=codigo_dep).first()
                        # Obtener stock
                        stock_model = StockModel.query.filter_by(medicine_id=medicine.id).first()
                        if ccan_dep_model and stock_model:
                            deposit_stock_model = DepositStockModel.query.filter_by(stock_id=stock_model.id,
                                                                                    deposit_id=ccan_dep_model.id).first()

                            # Verificacion de duplicidad
                            dispatch_medications_model = DispatchMedicationsModel.query.filter_by(
                                date=dispatch_medication.get('fecha_hora'), deposit_stock_id=deposit_stock_model.id,
                                patient_id=patient_id).first()
                            if not dispatch_medications_model:
                                dispatch_medications_model = DispatchMedicationsModel()
                                dispatch_medications_model.deposit_stock_id = deposit_stock_model.id
                                dispatch_medications_model.patient_id = patient_id
                                dispatch_medications_model.medicine_id = medicine.id
                                dispatch_medications_model.quantity = dispatch_medication.get('cantidad')
                                dispatch_medications_model.origin = OriginsCode.SICIAP.value
                                dispatch_medications_model.user_create = 'Interoperabilidad'
                                dispatch_medications_model.date = dispatch_medication.get('fecha_hora')
                                db.session.add(dispatch_medications_model)

                                # Registro de log
                                log_interoperability(operacion='Interoperar Entrega de Medicamentos a Pacientes',
                                                     origen=OriginsCode.HIS.value, data=dispatch_medication)

            # Se confirman todos los cambios
            db.session.commit()
            return {'message': 'success'}, 200
    except Exception as err:
        # Se revierte los cambios
        db.session.rollback()

        msg = f"Ocurrió un error al registrar consumo de medicamento. Detalle: {err.__cause__}"
        logging.error(msg, exc_info=err)
        return {"message": msg}, 500


def sync_patient_dispatch_medication_his(patient_id):
    patient = PatientModel.find_by_id(patient_id)
    if not patient:
        return {'message': 'No se encuentra Patient'}, 404

    # Obtener usuario manual o por tarea automática
    try:
        user_create = get_jwt_identity()
    except:
        user_create = 'Interoperabilidad'

    patient_data = patient.json()
    patient_document = patient_data['document_number']
    patient_registration_date = patient.registration_date
    interoperabilidad_dao = InteroperabilidadDao()

    try:
        with db.session.no_autoflush:

            dispatch_medications_list = interoperabilidad_dao.get_patient_dispatch_medications_history(
                patient_document=patient_document,
                patient_registration_date=patient_registration_date)

            for dispatch_medication in dispatch_medications_list:
                # Get Deposit
                codigo_dep = str(dispatch_medication.get('codigo_sucursal'))
                ccan_dep_model = DepositModel.query.filter_by(code=codigo_dep).first()
                #Get med_code
                med_code = str(dispatch_medication.get('codigo_medicamento'))
                medicine_id = MedicineModel.query.filter_by(code=med_code).first()
                # Get stock
                stock_model = StockModel.query.filter_by(medicine_id=medicine_id.id).first()
                if ccan_dep_model:
                    if stock_model:
                        deposit_stock_model = DepositStockModel.query.filter_by(stock_id=stock_model.id,
                                                                            deposit_id=ccan_dep_model.id).first()
                        if not deposit_stock_model:
                            deposit_stock_model = DepositStockModel()
                            deposit_stock_model.deposit_id = ccan_dep_model.id
                            deposit_stock_model.stock_id = stock_model.id
                            deposit_stock_model.quantity = dispatch_medication.get('cantidad')
                            db.session.add(deposit_stock_model)
                            db.session.commit()

                    # Verificacion de duplicidad
                    dispatch_medications_model = DispatchMedicationsModel.query.filter_by(
                        date=dispatch_medication.get('fecha_hora'),
                        patient_id=patient_id).first()
                    if not dispatch_medications_model:
                        dispatch_medications_model = DispatchMedicationsModel()
                        dispatch_medications_model.patient_id = patient_id
                        if stock_model:
                            dispatch_medications_model.deposit_stock_id = deposit_stock_model.id
                        dispatch_medications_model.medicine_id = medicine_id.id
                        dispatch_medications_model.quantity = dispatch_medication.get('cantidad')
                        dispatch_medications_model.origin = OriginsCode.SICIAP.value
                        dispatch_medications_model.user_create = user_create
                        dispatch_medications_model.date = dispatch_medication.get('fecha_hora')
                        db.session.add(dispatch_medications_model)

                        # Registro de log
                        log_interoperability(operacion='Interoperar Entrega de Medicamentos a Pacientes',
                                                 origen=OriginsCode.SICIAP.value, data=dispatch_medication)

            # Se confirman todos los cambios
            db.session.commit()
            return {'message': 'success'}, 200
    except Exception as err:
        # Se revierte los cambios
        db.session.rollback()

        msg = f"Ocurrió un error al registrar consumo de medicamento. Detalle: {err.__cause__}"
        logging.error(msg, exc_info=err)
        return {"message": msg}, 500
