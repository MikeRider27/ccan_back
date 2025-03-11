import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.radiotherapy_treatment_plan import RadiotherapyTreatmentPlanModel
from utils import restrict, paginated_results
from security import check

class RadiotherapyTreatmentPlan(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('radiotherapy_id', type=int)
    parser.add_argument('treatment_plan_id', type=int)
    parser.add_argument('num_session', type=int)

    @jwt_required()
    @check('radiotherapy_treatment_plan_get')
    @swag_from('../swagger/radiotherapy_treatment_plan/get_radiotherapy_treatment_plan.yaml')
    def get(self, id):
        radiotherapy_treatment_plan = RadiotherapyTreatmentPlanModel.find_by_id(id)
        if radiotherapy_treatment_plan:
            return radiotherapy_treatment_plan.json()
        return {'message': _("RADIOTHERAPY_TREATMENT_PLAN_NOT_FOUND")}, 404

    @jwt_required()
    @check('radiotherapy_treatment_plan_update')
    @swag_from('../swagger/radiotherapy_treatment_plan/put_radiotherapy_treatment_plan.yaml')
    def put(self, id):
        radiotherapy_treatment_plan = RadiotherapyTreatmentPlanModel.find_by_id(id)
        if radiotherapy_treatment_plan:
            newdata = RadiotherapyTreatmentPlan.parser.parse_args()
            RadiotherapyTreatmentPlanModel.from_reqparse(radiotherapy_treatment_plan, newdata)
            radiotherapy_treatment_plan.save_to_db()
            return radiotherapy_treatment_plan.json()
        return {'message': _("RADIOTHERAPY_TREATMENT_PLAN_NOT_FOUND")}, 404

    @jwt_required()
    @check('radiotherapy_treatment_plan_delete')
    @swag_from('../swagger/radiotherapy_treatment_plan/delete_radiotherapy_treatment_plan.yaml')
    def delete(self, id):
        radiotherapy_treatment_plan = RadiotherapyTreatmentPlanModel.find_by_id(id)
        if radiotherapy_treatment_plan:
            radiotherapy_treatment_plan.delete_from_db()

        return {'message': _("RADIOTHERAPY_TREATMENT_PLAN_DELETED")}


class RadiotherapyTreatmentPlanList(Resource):

    @jwt_required()
    @check('radiotherapy_treatment_plan_list')
    @swag_from('../swagger/radiotherapy_treatment_plan/list_radiotherapy_treatment_plan.yaml')
    def get(self):
        query = RadiotherapyTreatmentPlanModel.query
        return paginated_results(query)

    @jwt_required()
    @check('radiotherapy_treatment_plan_insert')
    @swag_from('../swagger/radiotherapy_treatment_plan/post_radiotherapy_treatment_plan.yaml')
    def post(self):
        data = RadiotherapyTreatmentPlan.parser.parse_args()

        id = data.get('id')

        if id is not None and RadiotherapyTreatmentPlanModel.find_by_id(id):
            return {'message': _("RADIOTHERAPY_TREATMENT_PLAN_DUPLICATED").format(id)}, 400

        radiotherapy_treatment_plan = RadiotherapyTreatmentPlanModel(**data)
        try:
            radiotherapy_treatment_plan.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating radiotherapy treatment plan.', exc_info=e)
            return {"message": _("RADIOTHERAPY_TREATMENT_PLAN_CREATE_ERROR")}, 500

        return radiotherapy_treatment_plan.json(), 201


class RadiotherapyTreatmentPlanSearch(Resource):

    @jwt_required()
    @check('radiotherapy_treatment_plan_search')
    @swag_from('../swagger/radiotherapy_treatment_plan/search_radiotherapy_treatment_plan.yaml')
    def post(self):
        query = RadiotherapyTreatmentPlanModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: RadiotherapyTreatmentPlanModel.id == x)
            query = restrict(query, filters, 'radiotherapy_id', lambda x: RadiotherapyTreatmentPlanModel.radiotherapy_id == x)
            query = restrict(query, filters, 'treatment_plan_id', lambda x: RadiotherapyTreatmentPlanModel.treatment_plan_id == x)
            query = restrict(query, filters, 'num_session', lambda x: RadiotherapyTreatmentPlanModel.num_session == x)

        # default order
        query = query.order_by(RadiotherapyTreatmentPlanModel.id.desc())
        return paginated_results(query)
