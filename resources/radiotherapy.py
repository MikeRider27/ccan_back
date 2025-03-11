import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.radiotherapy import RadiotherapyModel
from models.radiotherapy_treatment_plan import RadiotherapyTreatmentPlanModel
from resources.treatment_plan import treatment_plan_finish
from security import check
from utils import restrict, paginated_results


class Radiotherapy(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('patient_id', type=int)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('nro_session', type=int)
    parser.add_argument('observation', type=str)
    parser.add_argument('session_state_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('technician', type=str)
    parser.add_argument('nurse', type=str)
    parser.add_argument('treatment_plan_list', type=list, location='json')

    @jwt_required()
    @check('radiotherapy_get')
    @swag_from('../swagger/radiotherapy/get_radiotherapy.yaml')
    def get(self, id):
        radiotherapy = RadiotherapyModel.find_by_id(id)
        if radiotherapy:
            return radiotherapy.json()
        return {'message': _("RADIOTHERAPY_NOT_FOUND")}, 404

    @jwt_required()
    @check('radiotherapy_update')
    @swag_from('../swagger/radiotherapy/put_radiotherapy.yaml')
    def put(self, id):
        radiotherapy = RadiotherapyModel.find_by_id(id)
        if radiotherapy:
            newdata = Radiotherapy.parser.parse_args()
            radiotherapy_treatment_plan_data_list = newdata['treatment_plan_list']
            RadiotherapyModel.from_reqparse(radiotherapy, newdata)

            # treatment_plan_list update
            radiotherapy_treatment_plan_list = []
            for radiotherapy_treatment_plan_data in radiotherapy_treatment_plan_data_list:
                del radiotherapy_treatment_plan_data['treatment_plan']
                if radiotherapy_treatment_plan_data.get('id', None):
                    radiotherapy_treatment_plan_model = RadiotherapyTreatmentPlanModel.find_by_id(radiotherapy_treatment_plan_data['id'])
                    RadiotherapyTreatmentPlanModel.from_reqparse(radiotherapy_treatment_plan_model, radiotherapy_treatment_plan_data)
                else:
                    radiotherapy_treatment_plan_model = RadiotherapyTreatmentPlanModel(**radiotherapy_treatment_plan_data)
                radiotherapy_treatment_plan_list.append(radiotherapy_treatment_plan_model)

            radiotherapy.treatment_plan_list = radiotherapy_treatment_plan_list

            radiotherapy.user_modify = get_jwt_identity()
            radiotherapy.date_modify = datetime.now()
            radiotherapy.save_to_db()

            # Verificar si el plan de tratamiento ha finalizado
            treatment_plan_finish(newdata.get('patient_id', None))

            return radiotherapy.json()
        return {'message': _("RADIOTHERAPY_NOT_FOUND")}, 404

    @jwt_required()
    @check('radiotherapy_delete')
    @swag_from('../swagger/radiotherapy/delete_radiotherapy.yaml')
    def delete(self, id):
        radiotherapy = RadiotherapyModel.find_by_id(id)
        if radiotherapy:
            radiotherapy.delete_from_db()

        return {'message': _("RADIOTHERAPY_DELETED")}


class RadiotherapyList(Resource):

    @jwt_required()
    @check('radiotherapy_list')
    @swag_from('../swagger/radiotherapy/list_radiotherapy.yaml')
    def get(self):
        query = RadiotherapyModel.query
        return paginated_results(query)

    @jwt_required()
    @check('radiotherapy_insert')
    @swag_from('../swagger/radiotherapy/post_radiotherapy.yaml')
    def post(self):
        data = Radiotherapy.parser.parse_args()

        id = data.get('id')

        if id is not None and RadiotherapyModel.find_by_id(id):
            return {'message': _("RADIOTHERAPY_DUPLICATED").format(id)}, 400

        # treatment_plan_list
        radiotherapy_treatment_plan_data_list = data['treatment_plan_list']
        del data['treatment_plan_list']

        radiotherapy = RadiotherapyModel(**data)

        # treatment_plan_list
        for radiotherapy_treatment_plan_data in radiotherapy_treatment_plan_data_list:
            del radiotherapy_treatment_plan_data['treatment_plan']
            radiotherapy_treatment_plan_model = RadiotherapyTreatmentPlanModel(**radiotherapy_treatment_plan_data)
            radiotherapy.treatment_plan_list.append(radiotherapy_treatment_plan_model)

        try:
            radiotherapy.user_create = get_jwt_identity()
            radiotherapy.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating radiotherapy.', exc_info=e)
            return {"message": _("RADIOTHERAPY_CREATE_ERROR")}, 500

        # Verificar si el plan de tratamiento ha finalizado
        patient_id = data.get('patient_id', None)
        treatment_plan_finish(patient_id)

        return radiotherapy.json(), 201


class RadiotherapySearch(Resource):

    @jwt_required()
    @check('radiotherapy_search')
    @swag_from('../swagger/radiotherapy/search_radiotherapy.yaml')
    def post(self):
        query = RadiotherapyModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: RadiotherapyModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: RadiotherapyModel.patient_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: RadiotherapyModel.hospital_id == x)
            query = restrict(query, filters, 'nro_session', lambda x: RadiotherapyModel.nro_session == x)
            query = restrict(query, filters, 'observation', lambda x: RadiotherapyModel.observation.contains(x))
            query = restrict(query, filters, 'session_state_id', lambda x: RadiotherapyModel.session_state_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(RadiotherapyModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: RadiotherapyModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(RadiotherapyModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: RadiotherapyModel.user_modify.contains(x))
            query = restrict(query, filters, 'doctor_id', lambda x: RadiotherapyModel.doctor_id == x)
            query = restrict(query, filters, 'technician', lambda x: RadiotherapyModel.technician.contains(x))
            query = restrict(query, filters, 'nurse', lambda x: RadiotherapyModel.nurse.contains(x))

        # default order
        query = query.order_by(RadiotherapyModel.id.desc())

        return paginated_results(query)
