import logging
import time
from datetime import datetime

from flask import current_app

from dao.patient_dao import PatientDao
from models.configuration import ConfigurationModel
from models.medicine import MedicineModel
from models.stock import StockModel
from resources.interoperabilidad import get_stock_movements, sync_stock_movements_from_siciap, sync_patient_sigap, \
    sync_patient_dispatch_medication_siciap, sync_patient_consultation_his
from utils import log_duration_execution


def sync_patient_sigap_task():
    """
    Función para la tarea programada sync_patient_sigap_task
    :return:
    """
    logging.info(f"Running task sync_patient_sigap_task... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    init = time.time()

    sync_patient_sigap()

    fin = time.time()
    duration_seg = fin - init
    log_duration_execution(task_name='sync_patient_sigap_task', duration_seg=duration_seg)


def sync_patient_consultation_his_task():
    """
        Función para la tarea programada sync_patient_consultation_his_task
        :return:
        """
    logging.info(f"Running task sync_patient_consultation_his_task... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    init = time.time()

    # Se obtiene la lista de pacientes
    patient_dao = PatientDao()
    patient_list = patient_dao.get_patients_document()

    for patient_data in patient_list:
        patient_id = patient_data.get('patient_id')
        sync_patient_consultation_his(patient_id=patient_id)

    fin = time.time()
    duration_seg = fin - init
    log_duration_execution(task_name='sync_patient_consultation_his_task', duration_seg=duration_seg)


def sync_patient_dispatch_medication_siciap_task():
    """
    Función para la tarea programada sync_patient_dispatch_medication_siciap_task
    :return:
    """
    logging.info(
        f"Running task sync_patient_dispatch_medication_siciap_task... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    init = time.time()

    sync_patient_dispatch_medication_siciap()

    fin = time.time()
    duration_seg = fin - init
    log_duration_execution(task_name='sync_patient_dispatch_medication_siciap_task', duration_seg=duration_seg)


def sync_inventory_siciap_task():
    """
    Función para la tarea programada sync_inventory_siciap_task
    :return:
    """
    logging.info(f"Running task sync_inventory_siciap_task... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    init = time.time()

    # Se obtiene los medicamentos en seguimiento
    stock_list = StockModel.query.join(MedicineModel).filter_by(stock_control=True).all()

    # Se itera por cada medicamento
    for stock in stock_list:
        stock_inter_data = get_stock_movements(stock.id)
        sync_stock_movements_from_siciap(stock.id, stock_inter_data)

    fin = time.time()
    duration_seg = fin - init
    log_duration_execution(task_name='sync_inventory_siciap_task', duration_seg=duration_seg)


# Lógica para obtener el horario de ejecución desde la base de datos
def get_run_time_from_db():
    try:
        # Consulta BD
        config_data: ConfigurationModel = ConfigurationModel.query.filter_by(name='SCHEDULED_TASKS_TIME',
                                                                             code='STT').first()
        str_hour = config_data.value
        hour = datetime.strptime(str_hour, '%H:%M').time()
        # logging.info(f"The scheduled tasks will run at {str_hour}")
    except Exception as err:
        # logging.error(f"Error retrieving scheduled tasks time from the database. Detail: {err._cause_}")
        str_hour = '01:00'  # Default time
        hour = datetime.strptime(str_hour, '%H:%M').time()

    return hour


# Función para la tarea principal
def task_manager(app):
    with app.app_context():
        logging.info(f"Running Task Manager...  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        config_active = ConfigurationModel.query.filter_by(code='IS', value='ACTIVE').first()
        if config_active:
            # Run all tasks
            try:
                sync_patient_sigap_task()
                sync_patient_consultation_his_task()
                sync_patient_dispatch_medication_siciap_task()
                sync_inventory_siciap_task()
            except Exception as error:
                logging.error(error)
        else:
            logging.info('The interoperability services are not enabled.')
