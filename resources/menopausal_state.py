import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func

from models.menopausal_state import MenopausalStateModel
from utils import restrict, paginated_results
from security import check


class MenopausalState(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('code', type=str)

    @jwt_required()
    @check('menopausal_state_get')
    @swag_from('../swagger/menopausal_state/get_menopausal_state.yaml')
    def get(self, id):
        menopausal_state = MenopausalStateModel.find_by_id(id)
        if menopausal_state:
            return menopausal_state.json()
        return {'message': _("MENOPAUSAL_STATE_NOT_FOUND")}, 404

    @jwt_required()
    @check('menopausal_state_update')
    @swag_from('../swagger/menopausal_state/put_menopausal_state.yaml')
    def put(self, id):
        menopausal_state = MenopausalStateModel.find_by_id(id)
        if menopausal_state:
            newdata = MenopausalState.parser.parse_args()
            MenopausalStateModel.from_reqparse(menopausal_state, newdata)
            menopausal_state.save_to_db()
            return menopausal_state.json()
        return {'message': _("MENOPAUSAL_STATE_NOT_FOUND")}, 404

    @jwt_required()
    @check('menopausal_state_delete')
    @swag_from('../swagger/menopausal_state/delete_menopausal_state.yaml')
    def delete(self, id):
        menopausal_state = MenopausalStateModel.find_by_id(id)
        if menopausal_state:
            menopausal_state.delete_from_db()

        return {'message': _("MENOPAUSAL_STATE_DELETED")}


class MenopausalStateList(Resource):

    @jwt_required()
    @check('menopausal_state_list')
    @swag_from('../swagger/menopausal_state/list_menopausal_state.yaml')
    def get(self):
        query = MenopausalStateModel.query
        return paginated_results(query)

    @jwt_required()
    @check('menopausal_state_insert')
    @swag_from('../swagger/menopausal_state/post_menopausal_state.yaml')
    def post(self):
        data = MenopausalState.parser.parse_args()

        id = data.get('id')

        if id is not None and MenopausalStateModel.find_by_id(id):
            return {'message': _("MENOPAUSAL_STATE_DUPLICATED").format(id)}, 400

        menopausal_state = MenopausalStateModel(**data)
        try:
            menopausal_state.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating menopausal state.', exc_info=e)
            return {"message": _("MENOPAUSAL_STATE_CREATE_ERROR")}, 500

        return menopausal_state.json(), 201


class MenopausalStateSearch(Resource):

    @jwt_required()
    @check('menopausal_state_search')
    @swag_from('../swagger/menopausal_state/search_menopausal_state.yaml')
    def post(self):
        query = MenopausalStateModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MenopausalStateModel.id == x)
            query = restrict(query, filters, 'description', lambda x: func.lower(MenopausalStateModel.description).contains((x)))
            query = restrict(query, filters, 'code', lambda x: func.lower(MenopausalStateModel.code).contains((x)))

        return paginated_results(query)
