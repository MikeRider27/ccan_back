import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.type_treatment import TypeTreatmentModel
from security import check
from utils import restrict, paginated_results


class TypeTreatment(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('code', type=str)

    @jwt_required()
    @check('type_treatment_get')
    @swag_from('../swagger/type_treatment/get_type_treatment.yaml')
    def get(self, id):
        type_treatment = TypeTreatmentModel.find_by_id(id)
        if type_treatment:
            return type_treatment.json()
        return {'message': _("TREATMENT_TYPE_NOT_FOUND")}, 404

    @jwt_required()
    @check('type_treatment_update')
    @swag_from('../swagger/type_treatment/put_type_treatment.yaml')
    def put(self, id):
        type_treatment = TypeTreatmentModel.find_by_id(id)
        if type_treatment:
            newdata = TypeTreatment.parser.parse_args()
            TypeTreatmentModel.from_reqparse(type_treatment, newdata)
            type_treatment.save_to_db()
            return type_treatment.json()
        return {'message': _("TREATMENT_TYPE_NOT_FOUND")}, 404

    @jwt_required()
    @check('type_treatment_delete')
    @swag_from('../swagger/type_treatment/delete_type_treatment.yaml')
    def delete(self, id):
        type_treatment = TypeTreatmentModel.find_by_id(id)
        if type_treatment:
            type_treatment.delete_from_db()

        return {'message': _("TREATMENT_TYPE_DELETED")}


class TypeTreatmentList(Resource):

    @jwt_required()
    @check('type_treatment_list')
    @swag_from('../swagger/type_treatment/list_type_treatment.yaml')
    def get(self):
        query = TypeTreatmentModel.query
        return paginated_results(query)

    @jwt_required()
    @check('type_treatment_insert')
    @swag_from('../swagger/type_treatment/post_type_treatment.yaml')
    def post(self):
        data = TypeTreatment.parser.parse_args()

        id = data.get('id')

        if id is not None and TypeTreatmentModel.find_by_id(id):
            return {'message': _("TREATMENT_TYPE_DUPLICATED").format(id)}, 400

        type_treatment = TypeTreatmentModel(**data)
        try:
            type_treatment.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating type treatment.', exc_info=e)
            return {"message": _("TREATMENT_TYPE_CREATE_ERROR")}, 500

        return type_treatment.json(), 201


class TypeTreatmentSearch(Resource):

    @jwt_required()
    @check('type_treatment_search')
    @swag_from('../swagger/type_treatment/search_type_treatment.yaml')
    def post(self):
        query = TypeTreatmentModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: TypeTreatmentModel.id == x)
            query = restrict(query, filters, 'description', lambda x: func.lower(TypeTreatmentModel.description).contains(func.lower(x)))
            query = restrict(query, filters, 'code', lambda x: func.lower(TypeTreatmentModel.code).contains(func.lower(x)))

        return paginated_results(query)
