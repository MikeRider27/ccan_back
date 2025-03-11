import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.follow_up_treatment_plan import FollowUpTreatmentPlanModel
from utils import restrict, paginated_results
from security import check


class FollowUpTreatmentPlan(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('follow_up_id', type=int)
    parser.add_argument('treatment_plan_id', type=int)

    @jwt_required()
    @check('follow_up_treatment_plan_get')
    @swag_from('../swagger/follow_up_treatment_plan/get_follow_up_treatment_plan.yaml')
    def get(self, id):
        follow_up_treatment_plan = FollowUpTreatmentPlanModel.find_by_id(id)
        if follow_up_treatment_plan:
            return follow_up_treatment_plan.json()
        return {'message': _("FOLLOW_UP_TREATMENT_PLAN_NOT_FOUND")}, 404

    @jwt_required()
    @check('follow_up_treatment_plan_update')
    @swag_from('../swagger/follow_up_treatment_plan/put_follow_up_treatment_plan.yaml')
    def put(self, id):
        follow_up_treatment_plan = FollowUpTreatmentPlanModel.find_by_id(id)
        if follow_up_treatment_plan:
            newdata = FollowUpTreatmentPlan.parser.parse_args()
            FollowUpTreatmentPlanModel.from_reqparse(follow_up_treatment_plan, newdata)
            follow_up_treatment_plan.save_to_db()
            return follow_up_treatment_plan.json()
        return {'message': _("FOLLOW_UP_TREATMENT_PLAN_NOT_FOUND")}, 404

    @jwt_required()
    @check('follow_up_treatment_plan_delete')
    @swag_from('../swagger/follow_up_treatment_plan/delete_follow_up_treatment_plan.yaml')
    def delete(self, id):
        follow_up_treatment_plan = FollowUpTreatmentPlanModel.find_by_id(id)
        if follow_up_treatment_plan:
            follow_up_treatment_plan.delete_from_db()

        return {'message': _("FOLLOW_UP_TREATMENT_PLAN_DELETED")}


class FollowUpTreatmentPlanList(Resource):

    @jwt_required()
    @check('follow_up_treatment_plan_list')
    @swag_from('../swagger/follow_up_treatment_plan/list_follow_up_treatment_plan.yaml')
    def get(self):
        query = FollowUpTreatmentPlanModel.query
        return paginated_results(query)

    @jwt_required()
    @check('follow_up_treatment_plan_insert')
    @swag_from('../swagger/follow_up_treatment_plan/post_follow_up_treatment_plan.yaml')
    def post(self):
        data = FollowUpTreatmentPlan.parser.parse_args()

        id = data.get('id')

        if id is not None and FollowUpTreatmentPlanModel.find_by_id(id):
            return {'message': _("FOLLOW_UP_TREATMENT_PLAN_DUPLICATED").format(id)}, 400

        follow_up_treatment_plan = FollowUpTreatmentPlanModel(**data)
        try:
            follow_up_treatment_plan.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating follow up treatment plan.', exc_info=e)
            return {"message": _("FOLLOW_UP_TREATMENT_PLAN_CREATE_ERROR")}, 500

        return follow_up_treatment_plan.json(), 201


class FollowUpTreatmentPlanSearch(Resource):

    @jwt_required()
    @check('follow_up_treatment_plan_search')
    @swag_from('../swagger/follow_up_treatment_plan/search_follow_up_treatment_plan.yaml')
    def post(self):
        query = FollowUpTreatmentPlanModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: FollowUpTreatmentPlanModel.id == x)
            query = restrict(query, filters, 'follow_up_id', lambda x: FollowUpTreatmentPlanModel.follow_up_id == x)
            query = restrict(query, filters, 'treatment_plan_id', lambda x: FollowUpTreatmentPlanModel.treatment_plan_id == x)

        # default order
        query = query.order_by(FollowUpTreatmentPlanModel.id.desc())
        return paginated_results(query)
