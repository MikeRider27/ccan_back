import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.medicine_chemotherapy import MedicineChemotherapyModel
from utils import restrict, paginated_results
from security import check


class MedicineChemotherapy(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('chemotherapy_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('observation', type=str)
    parser.add_argument('dose', type=float)
    parser.add_argument('presentation', type=str)
    parser.add_argument('concentration', type=str)

    @jwt_required()
    @check('medicine_chemotherapy_get')
    @swag_from('../swagger/medicine_chemotherapy/get_medicine_chemotherapy.yaml')
    def get(self, id):
        medicine_chemotherapy = MedicineChemotherapyModel.find_by_id(id)
        if medicine_chemotherapy:
            return medicine_chemotherapy.json()
        return {'message': _("MEDICINE_CHEMOTHERAPY_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_chemotherapy_update')
    @swag_from('../swagger/medicine_chemotherapy/put_medicine_chemotherapy.yaml')
    def put(self, id):
        medicine_chemotherapy = MedicineChemotherapyModel.find_by_id(id)
        if medicine_chemotherapy:
            newdata = MedicineChemotherapy.parser.parse_args()
            MedicineChemotherapyModel.from_reqparse(medicine_chemotherapy, newdata)
            medicine_chemotherapy.save_to_db()
            return medicine_chemotherapy.json()
        return {'message': _("MEDICINE_CHEMOTHERAPY_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_chemotherapy_delete')
    @swag_from('../swagger/medicine_chemotherapy/delete_medicine_chemotherapy.yaml')
    def delete(self, id):
        medicine_chemotherapy = MedicineChemotherapyModel.find_by_id(id)
        if medicine_chemotherapy:
            medicine_chemotherapy.delete_from_db()

        return {'message': _("MEDICINE_CHEMOTHERAPY_DELETED")}


class MedicineChemotherapyList(Resource):

    @jwt_required()
    @check('medicine_chemotherapy_list')
    @swag_from('../swagger/medicine_chemotherapy/list_medicine_chemotherapy.yaml')
    def get(self):
        query = MedicineChemotherapyModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medicine_chemotherapy_insert')
    @swag_from('../swagger/medicine_chemotherapy/post_medicine_chemotherapy.yaml')
    def post(self):
        data = MedicineChemotherapy.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicineChemotherapyModel.find_by_id(id):
            return {'message': _("MEDICINE_CHEMOTHERAPY_DUPLICATED").format(id)}, 400

        medicine_chemotherapy = MedicineChemotherapyModel(**data)
        try:
            medicine_chemotherapy.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating medicine chemotherapy.', exc_info=e)
            return {"message": _("MEDICINE_CHEMOTHERAPY_CREATE_ERROR")}, 500

        return medicine_chemotherapy.json(), 201


class MedicineChemotherapySearch(Resource):

    @jwt_required()
    @check('medicine_chemotherapy_search')
    @swag_from('../swagger/medicine_chemotherapy/search_medicine_chemotherapy.yaml')
    def post(self):
        query = MedicineChemotherapyModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MedicineChemotherapyModel.id == x)
            query = restrict(query, filters, 'medicine_id', lambda x: MedicineChemotherapyModel.medicine_id == x)
            query = restrict(query, filters, 'chemotherapy_id', lambda x: MedicineChemotherapyModel.chemotherapy_id == x)
            query = restrict(query, filters, 'observation', lambda x: MedicineChemotherapyModel.observation.contains(x))
            query = restrict(query, filters, 'presentation', lambda x: MedicineChemotherapyModel.presentation.contains(x))
            query = restrict(query, filters, 'concentration', lambda x: MedicineChemotherapyModel.concentration.contains(x))

        # default order
        query = query.order_by(MedicineChemotherapyModel.id.desc())
        return paginated_results(query)
