import logging
from threading import Thread

from flasgger import swag_from
from flask import current_app
from flask_restful import Resource

from scheduled_tasks import sync_inventory_siciap_task, sync_patient_sigap_task, \
    sync_patient_dispatch_medication_siciap_task, sync_patient_consultation_his_task, task_manager


class InteroperabilidadSyncPatientSigapTask(Resource):
    @swag_from('../swagger/interoperabilidad/get_sync_patient_sigap_task.yaml')
    def get(self):
        sync_patient_sigap_task()
        return {'message': 'success'}, 200


class InteroperabilidadSyncPatientConsultationHisTask(Resource):
    @swag_from('../swagger/interoperabilidad/get_sync_patient_consultation_his_task.yaml')
    def get(self):
        sync_patient_consultation_his_task()
        return {'message': 'success'}, 200


class InteroperabilidadSyncPatientDispatchMedicationSiciapTask(Resource):
    @swag_from('../swagger/interoperabilidad/get_sync_patient_dispatch_medication_siciap_task.yaml')
    def get(self):
        sync_patient_dispatch_medication_siciap_task()
        return {'message': 'success'}, 200


class InteroperabilidadSyncInventorySiciapTask(Resource):
    @swag_from('../swagger/interoperabilidad/get_sync_inventory_siciap_task.yaml')
    def get(self):
        sync_inventory_siciap_task()
        return {'message': 'success'}, 200


class InteroperabilidadSyncTaskManager(Resource):
    @swag_from('../swagger/interoperabilidad/get_sync_task_manager.yaml')
    def get(self):
        # Captura el contexto de la aplicación
        app = current_app._get_current_object()

        logging.info("Scheduled Interoperability Tasks Daemon Started")
        start_scheduled_tasks_thread = Thread(target=task_manager, args=(app,))
        start_scheduled_tasks_thread.start()
        return {'message': 'success'}, 200
