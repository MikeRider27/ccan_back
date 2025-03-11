import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.specialty import SpecialtyModel
from security import check
from utils import restrict, paginated_results


class Specialty(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('origin', type=str)

    @jwt_required()
    @check('specialty_get')
    @swag_from('../swagger/specialty/get_specialty.yaml')
    def get(self, id):
        specialty = SpecialtyModel.find_by_id(id)
        if specialty:
            return specialty.json()
        return {'message': _("SPECIALITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('specialty_update')
    @swag_from('../swagger/specialty/put_specialty.yaml')
    def put(self, id):
        specialty = SpecialtyModel.find_by_id(id)
        if specialty:
            newdata = Specialty.parser.parse_args()
            SpecialtyModel.from_reqparse(specialty, newdata)
            specialty.save_to_db()
            return specialty.json()
        return {'message': _("SPECIALITY_NOT_FOUND")}, 404

    @jwt_required()
    @check('specialty_delete')
    @swag_from('../swagger/specialty/delete_specialty.yaml')
    def delete(self, id):
        specialty = SpecialtyModel.find_by_id(id)
        if specialty:
            specialty.delete_from_db()

        return {'message': _("SPECIALITY_DELETED")}


class SpecialtyList(Resource):

    @jwt_required()
    @check('specialty_list')
    @swag_from('../swagger/specialty/list_specialty.yaml')
    def get(self):
        query = SpecialtyModel.query
        return paginated_results(query)

    @jwt_required()
    @check('specialty_insert')
    @swag_from('../swagger/specialty/post_specialty.yaml')
    def post(self):
        data = Specialty.parser.parse_args()

        id = data.get('id')

        if id is not None and SpecialtyModel.find_by_id(id):
            return {'message': _("SPECIALITY_DUPLICATED").format(id)}, 400

        specialty = SpecialtyModel(**data)
        try:
            specialty.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating speciality.', exc_info=e)
            return {"message": _("SPECIALITY_CREATE_ERROR")}, 500

        return specialty.json(), 201


class SpecialtySearch(Resource):

    @jwt_required()
    @check('specialty_search')
    @swag_from('../swagger/specialty/search_specialty.yaml')
    def post(self):
        query = SpecialtyModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: SpecialtyModel.id == x)
            query = restrict(query, filters, 'description', lambda x: func.lower(SpecialtyModel.description).contains(func.lower(x)))
            query = restrict(query, filters, 'origin', lambda x: func.lower(SpecialtyModel.origin).contains(func.lower(x)))

        return paginated_results(query)
