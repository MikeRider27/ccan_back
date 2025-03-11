import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.medicine_treatment_plan import MedicineTreatmentPlanModel
from utils import restrict, paginated_results
from security import check


class MedicineTreatmentPlan(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('treatment_order_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('observation', type=str)
    parser.add_argument('dose', type=float)
    parser.add_argument('presentation', type=str)
    parser.add_argument('concentration', type=str)

    @jwt_required()
    @check('medicine_treatment_plan_get')
    @swag_from('../swagger/medicine_treatment_plan/get_medicine_treatment_plan.yaml')
    def get(self, id):
        medicine_treatment_plan = MedicineTreatmentPlanModel.find_by_id(id)
        if medicine_treatment_plan:
            return medicine_treatment_plan.json()
        return {'message': _("MEDICINE_TREATMENT_PLAN_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_treatment_plan_update')
    @swag_from('../swagger/medicine_treatment_plan/put_medicine_treatment_plan.yaml')
    def put(self, id):
        medicine_treatment_plan = MedicineTreatmentPlanModel.find_by_id(id)
        if medicine_treatment_plan:
            newdata = MedicineTreatmentPlan.parser.parse_args()
            MedicineTreatmentPlanModel.from_reqparse(medicine_treatment_plan, newdata)
            medicine_treatment_plan.save_to_db()
            return medicine_treatment_plan.json()
        return {'message': _("MEDICINE_TREATMENT_PLAN_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_treatment_plan_delete')
    @swag_from('../swagger/medicine_treatment_plan/delete_medicine_treatment_plan.yaml')
    def delete(self, id):
        medicine_treatment_plan = MedicineTreatmentPlanModel.find_by_id(id)
        if medicine_treatment_plan:
            medicine_treatment_plan.delete_from_db()

        return {'message': _("MEDICINE_TREATMENT_PLAN_DELETED")}


class MedicineTreatmentPlanList(Resource):

    @jwt_required()
    @check('medicine_treatment_plan_list')
    @swag_from('../swagger/medicine_treatment_plan/list_medicine_treatment_plan.yaml')
    def get(self):
        query = MedicineTreatmentPlanModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medicine_treatment_plan_insert')
    @swag_from('../swagger/medicine_treatment_plan/post_medicine_treatment_plan.yaml')
    def post(self):
        data = MedicineTreatmentPlan.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicineTreatmentPlanModel.find_by_id(id):
            return {'message': _("MEDICINE_TREATMENT_PLAN_DUPLICATED").format(id)}, 400

        medicine_treatment_plan = MedicineTreatmentPlan(**data)
        try:
            medicine_treatment_plan.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating medicine treatment plan.', exc_info=e)
            return {"message": _("MEDICINE_TREATMENT_PLAN_CREATE_ERROR")}, 500

        return medicine_treatment_plan.json(), 201


class MedicineTreatmentPlanSearch(Resource):

    @jwt_required()
    @check('medicine_treatment_plan_search')
    @swag_from('../swagger/medicine_treatment_plan/search_medicine_treatment_plan.yaml')
    def post(self):
        query = MedicineTreatmentPlanModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MedicineTreatmentPlanModel.id == x)
            query = restrict(query, filters, 'medicine_id', lambda x: MedicineTreatmentPlanModel.medicine_id == x)
            query = restrict(query, filters, 'medication_order_id', lambda x: MedicineTreatmentPlanModel.medication_order_id == x)
            query = restrict(query, filters, 'quantity', lambda x: MedicineTreatmentPlanModel.quantity == x)
            query = restrict(query, filters, 'observation', lambda x: MedicineTreatmentPlanModel.observation.contains(x))
            query = restrict(query, filters, 'presentation',
                             lambda x: MedicineTreatmentPlanModel.presentation.contains(x))
            query = restrict(query, filters, 'concentration',
                             lambda x: MedicineTreatmentPlanModel.concentration.contains(x))
        return paginated_results(query)
