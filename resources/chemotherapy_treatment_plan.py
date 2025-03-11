import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.chemotherapy_treatment_plan import ChemotherapyTreatmentPlanModel
from utils import restrict, paginated_results
from security import check


class ChemotherapyTreatmentPlan(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('chemotherapy_id', type=int)
    parser.add_argument('treatment_plan_id', type=int)
    parser.add_argument('num_session', type=int)

    @jwt_required()
    @check('chemotherapy_treatment_plan_get')
    @swag_from('../swagger/chemotherapy_treatment_plan/get_chemotherapy_treatment_plan.yaml')
    def get(self, id):
        chemotherapy_treatment_plan = ChemotherapyTreatmentPlanModel.find_by_id(id)
        if chemotherapy_treatment_plan:
            return chemotherapy_treatment_plan.json()
        return {'message': _("CTP_NOT_FOUND")}, 404

    @jwt_required()
    @check('chemotherapy_treatment_plan_update')
    @swag_from('../swagger/chemotherapy_treatment_plan/put_chemotherapy_treatment_plan.yaml')
    def put(self, id):
        chemotherapy_treatment_plan = ChemotherapyTreatmentPlanModel.find_by_id(id)
        if chemotherapy_treatment_plan:
            newdata = ChemotherapyTreatmentPlan.parser.parse_args()
            ChemotherapyTreatmentPlanModel.from_reqparse(chemotherapy_treatment_plan, newdata)
            chemotherapy_treatment_plan.save_to_db()
            return chemotherapy_treatment_plan.json()
        return {'message': _("CTP_NOT_FOUND")}, 404

    @jwt_required()
    @check('chemotherapy_treatment_plan_delete')
    @swag_from('../swagger/chemotherapy_treatment_plan/delete_chemotherapy_treatment_plan.yaml')
    def delete(self, id):
        chemotherapy_treatment_plan = ChemotherapyTreatmentPlanModel.find_by_id(id)
        if chemotherapy_treatment_plan:
            chemotherapy_treatment_plan.delete_from_db()

        return {'message': _("CTP_DELETED")}


class ChemotherapyTreatmentPlanList(Resource):

    @jwt_required()
    @check('chemotherapy_treatment_plan_list')
    @swag_from('../swagger/chemotherapy_treatment_plan/list_chemotherapy_treatment_plan.yaml')
    def get(self):
        query = ChemotherapyTreatmentPlanModel.query
        return paginated_results(query)

    @jwt_required()
    @check('chemotherapy_treatment_plan_insert')
    @swag_from('../swagger/chemotherapy_treatment_plan/post_chemotherapy_treatment_plan.yaml')
    def post(self):
        data = ChemotherapyTreatmentPlan.parser.parse_args()

        id = data.get('id')

        if id is not None and ChemotherapyTreatmentPlanModel.find_by_id(id):
            return {'message': _("CTP_DUPLICATED").format(id)}, 400

        chemotherapy_treatment_plan = ChemotherapyTreatmentPlanModel(**data)
        try:
            chemotherapy_treatment_plan.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating Chemotherapy treatment plan.', exc_info=e)
            return {"message": _("CTP_CREATE_ERROR")}, 500

        return chemotherapy_treatment_plan.json(), 201


class ChemotherapyTreatmentPlanSearch(Resource):

    @jwt_required()
    @check('chemotherapy_treatment_plan_search')
    @swag_from('../swagger/chemotherapy_treatment_plan/search_chemotherapy_treatment_plan.yaml')
    def post(self):
        query = ChemotherapyTreatmentPlanModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: ChemotherapyTreatmentPlanModel.id == x)
            query = restrict(query, filters, 'chemotherapy_id', lambda x: ChemotherapyTreatmentPlanModel.chemotherapy_id == x)
            query = restrict(query, filters, 'treatment_plan_id', lambda x: ChemotherapyTreatmentPlanModel.treatment_plan_id == x)
            query = restrict(query, filters, 'num_session', lambda x: ChemotherapyTreatmentPlanModel.num_session == x)

        # default order
        query = query.order_by(ChemotherapyTreatmentPlanModel.id.desc())
        return paginated_results(query)
