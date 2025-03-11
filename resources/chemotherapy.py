import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.chemotherapy import ChemotherapyModel
from models.chemotherapy_treatment_plan import ChemotherapyTreatmentPlanModel
from models.medicine_chemotherapy import MedicineChemotherapyModel
from resources.treatment_plan import treatment_plan_finish
from security import check
from utils import restrict, paginated_results


class Chemotherapy(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('patient_id', type=int)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('nro_session', type=int)
    parser.add_argument('request_state_id', type=int)
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
    parser.add_argument('medicine_list', type=list, location='json')

    @jwt_required()
    @check('chemotherapy_get')
    @swag_from('../swagger/chemotherapy/get_chemotherapy.yaml')
    def get(self, id):
        chemotherapy = ChemotherapyModel.find_by_id(id)
        if chemotherapy:
            return chemotherapy.json()
        return {'message': _("CHEMOTHERAPY_NOT_FOUND")}, 404

    @jwt_required()
    @check('chemotherapy_update')
    @swag_from('../swagger/chemotherapy/put_chemotherapy.yaml')
    def put(self, id):
        chemotherapy: ChemotherapyModel = ChemotherapyModel.find_by_id(id)
        if chemotherapy:
            newdata = Chemotherapy.parser.parse_args()
            chemotherapy_treatment_plan_data_list = newdata['treatment_plan_list']
            chemotherapy_medicine_data_list = newdata['medicine_list']
            ChemotherapyModel.from_reqparse(chemotherapy, newdata)

            # treatment_plan_list update
            chemotherapy_treatment_plan_list = []
            for chemotherapy_treatment_plan_data in chemotherapy_treatment_plan_data_list:
                del chemotherapy_treatment_plan_data['treatment_plan']
                if chemotherapy_treatment_plan_data.get('id', None):
                    chemotherapy_treatment_plan_model = ChemotherapyTreatmentPlanModel.find_by_id(chemotherapy_treatment_plan_data['id'])
                    ChemotherapyTreatmentPlanModel.from_reqparse(chemotherapy_treatment_plan_model, chemotherapy_treatment_plan_data)
                else:
                    chemotherapy_treatment_plan_model = ChemotherapyTreatmentPlanModel(**chemotherapy_treatment_plan_data)
                chemotherapy_treatment_plan_list.append(chemotherapy_treatment_plan_model)
            chemotherapy.treatment_plan_list = chemotherapy_treatment_plan_list

            # medicine_list update
            chemotherapy_medicine_list = []
            for chemotherapy_medicine_data in chemotherapy_medicine_data_list:
                del chemotherapy_medicine_data['medicine']
                if chemotherapy_medicine_data.get('id', None):
                    chemotherapy_medicine_model = MedicineChemotherapyModel.find_by_id(chemotherapy_medicine_data['id'])
                    MedicineChemotherapyModel.from_reqparse(chemotherapy_medicine_model, chemotherapy_medicine_data)
                else:
                    chemotherapy_medicine_model = MedicineChemotherapyModel(**chemotherapy_medicine_data)
                chemotherapy_medicine_list.append(chemotherapy_medicine_model)
            chemotherapy.medicine_list = chemotherapy_medicine_list

            chemotherapy.user_modify = get_jwt_identity()
            chemotherapy.date_modify = datetime.now()
            chemotherapy.save_to_db()

            # Verificar si el plan de tratamiento ha finalizado
            treatment_plan_finish(newdata.get('patient_id', None))

            return chemotherapy.json()
        return {'message': _("CHEMOTHERAPY_NOT_FOUND")}, 404

    @jwt_required()
    @check('chemotherapy_delete')
    @swag_from('../swagger/chemotherapy/delete_chemotherapy.yaml')
    def delete(self, id):
        chemotherapy = ChemotherapyModel.find_by_id(id)
        if chemotherapy:
            chemotherapy.delete_from_db()

        return {'message': _("CHEMOTHERAPY_DELETED")}


class ChemotherapyList(Resource):

    @jwt_required()
    @check('chemotherapy_list')
    @swag_from('../swagger/chemotherapy/list_chemotherapy.yaml')
    def get(self):
        query = ChemotherapyModel.query
        return paginated_results(query)

    @jwt_required()
    @check('chemotherapy_insert')
    @swag_from('../swagger/chemotherapy/post_chemotherapy.yaml')
    def post(self):
        data = Chemotherapy.parser.parse_args()

        id = data.get('id')

        if id is not None and ChemotherapyModel.find_by_id(id):
            return {'message': _("CHEMOTHERAPY_DUPLICATED").format(id)}, 400

        # treatment_plan_list
        chemotherapy_treatment_plan_data_list = data['treatment_plan_list']
        del data['treatment_plan_list']

        # medicine_list
        chemotherapy_medicine_data_list = data['medicine_list']
        del data['medicine_list']

        chemotherapy = ChemotherapyModel(**data)

        # treatment_plan_list
        for chemotherapy_treatment_plan_data in chemotherapy_treatment_plan_data_list:
            del chemotherapy_treatment_plan_data['treatment_plan']
            chemotherapy_treatment_plan_model = ChemotherapyTreatmentPlanModel(**chemotherapy_treatment_plan_data)
            chemotherapy.treatment_plan_list.append(chemotherapy_treatment_plan_model)

        # medicine_list
        for chemotherapy_medicine_data in chemotherapy_medicine_data_list:
            del chemotherapy_medicine_data['medicine']
            chemotherapy_medicine_model = MedicineChemotherapyModel(**chemotherapy_medicine_data)
            chemotherapy.medicine_list.append(chemotherapy_medicine_model)

        try:
            chemotherapy.user_create = get_jwt_identity()
            chemotherapy.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating chemotherapy.', exc_info=e)
            return {"message": _("CHEMOTHERAPY_CREATE_ERROR")}, 500

        # Verificar si el plan de tratamiento ha finalizado
        patient_id = data.get('patient_id', None)
        treatment_plan_finish(patient_id)

        return chemotherapy.json(), 201


class ChemotherapySearch(Resource):

    @jwt_required()
    @check('chemotherapy_search')
    @swag_from('../swagger/chemotherapy/search_chemotherapy.yaml')
    def post(self):
        query = ChemotherapyModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: ChemotherapyModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: ChemotherapyModel.patient_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: ChemotherapyModel.hospital_id == x)
            query = restrict(query, filters, 'nro_session', lambda x: ChemotherapyModel.nro_session == x)
            query = restrict(query, filters, 'request_state_id', lambda x: ChemotherapyModel.request_state_id == x)
            query = restrict(query, filters, 'observation', lambda x: ChemotherapyModel.observation.contains(x))
            query = restrict(query, filters, 'session_state_id', lambda x: ChemotherapyModel.session_state_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(ChemotherapyModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: ChemotherapyModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(ChemotherapyModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: ChemotherapyModel.user_modify.contains(x))
            query = restrict(query, filters, 'doctor_id', lambda x: ChemotherapyModel.doctor_id == x)
            query = restrict(query, filters, 'technician', lambda x: ChemotherapyModel.technician.contains(x))
            query = restrict(query, filters, 'nurse', lambda x: ChemotherapyModel.nurse.contains(x))

        # default order
        query = query.order_by(ChemotherapyModel.id.desc())

        return paginated_results(query)
