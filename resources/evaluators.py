import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.evaluators import EvaluatorsModel
from utils import restrict, paginated_results
from security import check


class Evaluators(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('evaluation_id', type=int)
    parser.add_argument('evaluator_id', type=int)

    @jwt_required()
    @check('evaluators_get')
    @swag_from('../swagger/evaluators/get_evaluators.yaml')
    def get(self, id):
        evaluators = EvaluatorsModel.find_by_id(id)
        if evaluators:
            return evaluators.json()
        return {'message': _("EVALUATORS_NOT_FOUND")}, 404

    @jwt_required()
    @check('evaluators_update')
    @swag_from('../swagger/evaluators/put_evaluators.yaml')
    def put(self, id):
        evaluators = EvaluatorsModel.find_by_id(id)
        if evaluators:
            newdata = Evaluators.parser.parse_args()
            EvaluatorsModel.from_reqparse(evaluators, newdata)
            evaluators.save_to_db()
            return evaluators.json()
        return {'message': _("EVALUATORS_NOT_FOUND")}, 404

    @jwt_required()
    @check('evaluators_delete')
    @swag_from('../swagger/evaluators/delete_evaluators.yaml')
    def delete(self, id):
        evaluators = EvaluatorsModel.find_by_id(id)
        if evaluators:
            evaluators.delete_from_db()

        return {'message': _("EVALUATORS_DELETED")}


class EvaluatorsList(Resource):

    @jwt_required()
    @check('evaluators_list')
    @swag_from('../swagger/evaluators/list_evaluators.yaml')
    def get(self):
        query = EvaluatorsModel.query
        return paginated_results(query)

    @jwt_required()
    @check('evaluators_insert')
    @swag_from('../swagger/evaluators/post_evaluators.yaml')
    def post(self):
        data = Evaluators.parser.parse_args()

        id = data.get('id')

        if id is not None and EvaluatorsModel.find_by_id(id):
            return {'message': _("EVALUATORS_DUPLICATED").format(id)}, 400

        evaluators = EvaluatorsModel(**data)
        try:
            evaluators.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating evaluators.', exc_info=e)
            return {"message": _("EVALUATORS_CREATE_ERROR")}, 500

        return evaluators.json(), 201


class EvaluatorsSearch(Resource):

    @jwt_required()
    @check('evaluators_search')
    @swag_from('../swagger/evaluators/search_evaluators.yaml')
    def post(self):
        query = EvaluatorsModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: EvaluatorsModel.id == x)
            query = restrict(query, filters, 'evaluation_id', lambda x: EvaluatorsModel.evaluation_id == x)
            query = restrict(query, filters, 'evaluator_id', lambda x: EvaluatorsModel.evaluator_id == x)

        # default order
        query = query.order_by(EvaluatorsModel.id.desc())
        return paginated_results(query)
