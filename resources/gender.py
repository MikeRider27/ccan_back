import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.gender import GenderModel
from security import check
from utils import restrict, paginated_results

class Gender(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('code', type=str)

    @jwt_required()
    @check('gender_get')
    @swag_from('../swagger/gender/get_gender.yaml')
    def get(self, id):
        gender = GenderModel.find_by_id(id)
        if gender:
            return gender.json()
        return {'message': _("GENDER_NOT_FOUND")}, 404

    @jwt_required()
    @check('gender_update')
    @swag_from('../swagger/gender/put_gender.yaml')
    def put(self, id):
        gender = GenderModel.find_by_id(id)
        if gender:
            newdata = Gender.parser.parse_args()
            GenderModel.from_reqparse(gender, newdata)
            gender.save_to_db()
            return gender.json()
        return {'message': _("GENDER_NOT_FOUND")}, 404

    @jwt_required()
    @check('gender_delete')
    @swag_from('../swagger/gender/delete_gender.yaml')
    def delete(self, id):
        gender = GenderModel.find_by_id(id)
        if gender:
            gender.delete_from_db()

        return {'message': _("GENDER_DELETED")}


class GenderList(Resource):

    @jwt_required()
    @check('gender_list')
    @swag_from('../swagger/gender/list_gender.yaml')
    def get(self):
        query = GenderModel.query
        return paginated_results(query)

    @jwt_required()
    @check('gender_insert')
    @swag_from('../swagger/gender/post_gender.yaml')
    def post(self):
        data = Gender.parser.parse_args()

        id = data.get('id')

        if id is not None and GenderModel.find_by_id(id):
            return {'message': _("GENDER_DUPLICATED").format(id)}, 400

        gender = GenderModel(**data)
        try:
            gender.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating gender.', exc_info=e)
            return {"message": _("GENDER_CREATE_ERROR")}, 500

        return gender.json(), 201


class GenderSearch(Resource):

    @jwt_required()
    @check('gender_search')
    @swag_from('../swagger/gender/search_gender.yaml')
    def post(self):
        query = GenderModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: GenderModel.id == x)
            query = restrict(query, filters, 'description', lambda x: func.lower(GenderModel.description).contains(func.lower(x)))
            query = restrict(query, filters, 'code', lambda x: func.lower(GenderModel.code).contains(func.lower(x)))

        return paginated_results(query)
