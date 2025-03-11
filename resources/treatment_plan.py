import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import and_
from flask_babel import _

from dao.treatment_plan_dao import TreatmentPlanDao
from models.chemotherapy import ChemotherapyModel
from models.chemotherapy_treatment_plan import ChemotherapyTreatmentPlanModel
from models.medicine_treatment_plan import MedicineTreatmentPlanModel
from models.parameter import ParameterModel
from models.periodicity import PeriodicityModel
from models.radiotherapy import RadiotherapyModel
from models.radiotherapy_treatment_plan import RadiotherapyTreatmentPlanModel
from models.treatment_plan import TreatmentPlanModel
from resources.patient import patient_update_state
from security import check
from utils import restrict, paginated_results, get_treatment_plan_dates


class TreatmentPlan(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('size', type=float)
    parser.add_argument('weight', type=float)
    parser.add_argument('sc', type=float)
    parser.add_argument('medical_visit_observation', type=str)
    parser.add_argument('cie_10_code_id', type=int)
    parser.add_argument('cie_o_morphology_id', type=int)
    parser.add_argument('cie_o_topography_id', type=int)
    parser.add_argument('cie_o_tumor_location_id', type=int)
    parser.add_argument('type_id', type=int)
    parser.add_argument('number_sessions', type=int)
    parser.add_argument('periodicity_id', type=int)
    parser.add_argument('date_first_cycle', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('date_last_cycle', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('observation', type=str)
    parser.add_argument('origin', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_modify', type=str)
    parser.add_argument('medicine_list', type=list, location='json')
    parser.add_argument('number', type=int)
    parser.add_argument('state_id', type=int)

    @jwt_required()
    @check('treatment_plan_get')
    @swag_from('../swagger/treatment_plan/get_treatment_plan.yaml')
    def get(self, id):
        treatment_plan = TreatmentPlanModel.find_by_id(id)
        if treatment_plan:
            return treatment_plan.json()
        return {'message': _('TREATMENT_PLAN_NOT_FOUND')}, 404

    @jwt_required()
    @check('treatment_plan_update')
    @swag_from('../swagger/treatment_plan/put_treatment_plan.yaml')
    def put(self, id):
        treatment_plan = TreatmentPlanModel.find_by_id(id)
        if treatment_plan:
            newdata = TreatmentPlan.parser.parse_args()
            medicine_treatment_plan_data_list = newdata['medicine_list']
            TreatmentPlanModel.from_reqparse(treatment_plan, newdata)

            # medicine_treatment_plan update
            medicine_treatment_plan_list = []
            for medicine_treatment_plan in medicine_treatment_plan_data_list:
                del medicine_treatment_plan['medicine']
                if 'id' in medicine_treatment_plan and medicine_treatment_plan['id']:
                    medicine_treatment_plan_model = MedicineTreatmentPlanModel.find_by_id(
                        medicine_treatment_plan['id'])
                    MedicineTreatmentPlanModel.from_reqparse(medicine_treatment_plan_model,
                                                             medicine_treatment_plan)
                else:
                    medicine_treatment_plan_model = MedicineTreatmentPlanModel(**medicine_treatment_plan)
                medicine_treatment_plan_list.append(medicine_treatment_plan_model)

            treatment_plan.medicine_list = medicine_treatment_plan_list

            treatment_plan.user_modify = get_jwt_identity()
            treatment_plan.date_modify = datetime.now()
            treatment_plan.save_to_db()
            return treatment_plan.json()
        return {'message': _('TREATMENT_PLAN_NOT_FOUND')}, 404

    @jwt_required()
    @check('treatment_plan_delete')
    @swag_from('../swagger/treatment_plan/delete_treatment_plan.yaml')
    def delete(self, id):
        treatment_plan = TreatmentPlanModel.find_by_id(id)
        if treatment_plan:
            treatment_plan.delete_from_db()

        return {'message': _('TREATMENT_PLAN_DELETED')}


class TreatmentPlanList(Resource):

    @jwt_required()
    @check('treatment_plan_list')
    @swag_from('../swagger/treatment_plan/list_treatment_plan.yaml')
    def get(self):
        query = TreatmentPlanModel.query
        return paginated_results(query)

    @jwt_required()
    @check('treatment_plan_insert')
    @swag_from('../swagger/treatment_plan/post_treatment_plan.yaml')
    def post(self):
        data = TreatmentPlan.parser.parse_args()

        id = data.get('id')

        if id is not None and TreatmentPlanModel.find_by_id(id):
            return {'message': _("_('TREATMENT_PLAN_DUPLICATED')").format(id)}, 400

        medicine_treatment_plan_data_list = data['medicine_list']
        del data['medicine_list']

        treatment_plan = TreatmentPlanModel(**data)

        for medicine_treatment_plan in medicine_treatment_plan_data_list:
            del medicine_treatment_plan['medicine']
            medicine_treatment_plan_model = MedicineTreatmentPlanModel(**medicine_treatment_plan)
            treatment_plan.medicine_list.append(medicine_treatment_plan_model)

        try:
            treatment_plan.user_create = get_jwt_identity()
            treatment_plan.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating treatment plan.', exc_info=e)
            return {"message": _("TREATMENT_PLAN_CREATE_ERROR")}, 500

        # LLamar evento de cambio de estado de paciente
        patient_update_state(data.get('patient_id', None))

        return treatment_plan.json(), 201


class TreatmentPlanSearch(Resource):

    @jwt_required()
    @check('treatment_plan_search')
    @swag_from('../swagger/treatment_plan/search_treatment_plan.yaml')
    def post(self):
        query = TreatmentPlanModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: TreatmentPlanModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: TreatmentPlanModel.patient_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: TreatmentPlanModel.hospital_id == x)
            query = restrict(query, filters, 'doctor_id', lambda x: TreatmentPlanModel.doctor_id == x)
            query = restrict(query, filters, 'medical_visit_observation', lambda x: TreatmentPlanModel.medical_visit_observation.contains(x))
            query = restrict(query, filters, 'cie_10_code_id', lambda x: TreatmentPlanModel.cie_10_code_id == x)
            query = restrict(query, filters, 'cie_o_morphology_id', lambda x: TreatmentPlanModel.cie_o_morphology_id == x)
            query = restrict(query, filters, 'cie_o_topography_id', lambda x: TreatmentPlanModel.cie_o_topography_id == x)
            query = restrict(query, filters, 'cie_o_tumor_location_id', lambda x: TreatmentPlanModel.cie_o_tumor_location_id == x)
            query = restrict(query, filters, 'type_id', lambda x: TreatmentPlanModel.type_id == x)
            query = restrict(query, filters, 'number_sessions', lambda x: TreatmentPlanModel.number_sessions == x)
            query = restrict(query, filters, 'periodicity_id', lambda x: TreatmentPlanModel.periodicity_id == x)
            query = restrict(query, filters, 'observation', lambda x: TreatmentPlanModel.observation.contains(x))
            query = restrict(query, filters, 'origin', lambda x: TreatmentPlanModel.origin.contains(x))
            query = restrict(query, filters, 'user_create', lambda x: TreatmentPlanModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: TreatmentPlanModel.user_modify.contains(x))
            query = restrict(query, filters, 'number', lambda x: TreatmentPlanModel.active == x)
            query = restrict(query, filters, 'state_id', lambda x: TreatmentPlanModel.state_id == x)

        # default order
        query = query.order_by(TreatmentPlanModel.id.desc())

        return paginated_results(query)


class TreatmentPlanPlanification(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('number_sessions', type=int)
    parser.add_argument('periodicity_id', type=int)
    parser.add_argument('date_first_cycle', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))

    @jwt_required()
    def post(self):
        newdata = TreatmentPlanPlanification.parser.parse_args()
        periodicity_id = newdata.get('periodicity_id', None)
        if not periodicity_id:
            return {"message": _("TREATMENT_PLAN_OBLIGATORY_PERIODICITY")}, 400
        number_sessions = newdata.get('number_sessions', None)
        if not number_sessions:
            return {"message": _("TREATMENT_PLAN_OBLIGATORY_SESSION")}, 400
        date_first_cycle = newdata.get('date_first_cycle', None)
        if not date_first_cycle:
            return {"message": _("TREATMENT_PLAN_OBLIGATORY_DATE")}, 400

        periodicity = PeriodicityModel.find_by_id(periodicity_id)
        periodicity = periodicity

        plan = get_treatment_plan_dates(date_first_cycle=date_first_cycle, periodicity=periodicity, number_sessions=number_sessions)

        return plan, 200


# TODO: preguntar cual es la regla para que una sesion este finalizada
def treatment_plan_finish(patient_id):
    if not patient_id:
        return

    tp_state_fin = ParameterModel.query.filter_by(domain='TREATMENT_PLAN_STATE', code='tret_pla_fin').first()
    tp_state_in_progress = ParameterModel.query.filter_by(domain='TREATMENT_PLAN_STATE', code='tret_pla_cur').first()
    treatment_plan_list = TreatmentPlanModel.query.filter_by(patient_id=patient_id, state_id=tp_state_in_progress.id).all()
    for treatment_plan in treatment_plan_list:
        # Si la sesion ya no esta finalizada
        if treatment_plan.state_id != tp_state_fin.id:
            if treatment_plan.type_treatment.code == 'CHEMOTHERAPY':
                chemo_request_aprob = ParameterModel.query.filter_by(domain='CHEMOTHERAPY_REQUEST_STATE', code='CHEM_REQ_APROB').first()
                chemo_session_fin = ParameterModel.query.filter_by(domain='CHEMOTHERAPY_SESSION_STATE', code='CHEM_SES_FIN').first()
                list_sessions = ChemotherapyModel.query\
                    .join(ChemotherapyTreatmentPlanModel, and_(ChemotherapyTreatmentPlanModel.chemotherapy_id == ChemotherapyModel.id, ChemotherapyTreatmentPlanModel.treatment_plan_id == treatment_plan.id))\
                    .filter(ChemotherapyModel.request_state_id == chemo_request_aprob.id, ChemotherapyModel.session_state_id == chemo_session_fin.id)\
                    .all()
                if len(list_sessions) == treatment_plan.number_sessions:
                    treatment_plan.state_id = tp_state_fin.id
                    treatment_plan.save_to_db()

            if treatment_plan.type_treatment.code == 'RADIOTHERAPY':
                radio_session_fin = ParameterModel.query.filter_by(domain='RADIOTHERAPY_SESSION_STATE', code='RADIO_SES_FIN').first()
                list_sessions = RadiotherapyModel.query\
                    .join(RadiotherapyTreatmentPlanModel, and_(RadiotherapyTreatmentPlanModel.radiotherapy_id == RadiotherapyModel.id, RadiotherapyTreatmentPlanModel.treatment_plan_id == treatment_plan.id)) \
                    .filter(RadiotherapyModel.session_state_id == radio_session_fin.id) \
                    .all()
                if len(list_sessions) == treatment_plan.number_sessions:
                    treatment_plan.state_id = tp_state_fin.id
                    treatment_plan.save_to_db()

    # Se actualiza estado del paciente
    patient_update_state(patient_id)


class TreatmentPlanNumber(Resource):
    @jwt_required()
    def get(self, patient_id):
        treatmentPlanDao = TreatmentPlanDao()
        number = treatmentPlanDao.get_number(patient_id)
        result = number.get('next', None)

        return result, 200
