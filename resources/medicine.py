import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func, and_, or_

from models.medicine import MedicineModel
from utils import paginated_results, restrict_collector
from security import check


class Medicine(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type=str)
    parser.add_argument('code', type=str)
    parser.add_argument('concentration', type=str)
    parser.add_argument('pharmaceutical_form', type=str)
    parser.add_argument('via_admin', type=str)
    parser.add_argument('presentation', type=str)
    parser.add_argument('code_dgc', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('stock_control', type=bool)
    parser.add_argument('generic_name', type=str)

    @jwt_required()
    @check('medicine_get')
    @swag_from('../swagger/medicine/get_medicine.yaml')
    def get(self, id):
        medicine = MedicineModel.find_by_id(id)
        if medicine:
            return medicine.json()
        return {'message': _("MEDICINE_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_update')
    @swag_from('../swagger/medicine/put_medicine.yaml')
    def put(self, id):
        medicine = MedicineModel.find_by_id(id)
        if medicine:
            newdata = Medicine.parser.parse_args()
            MedicineModel.from_reqparse(medicine, newdata)

            medicine.user_modify = get_jwt_identity()
            medicine.date_modify = datetime.now()
            medicine.save_to_db()
            return medicine.json()
        return {'message': _("MEDICINE_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_delete')
    @swag_from('../swagger/medicine/delete_medicine.yaml')
    def delete(self, id):
        medicine = MedicineModel.find_by_id(id)
        if medicine:
            medicine.delete_from_db()

        return {'message': _("MEDICINE_DELETED")}


class MedicineList(Resource):

    @jwt_required()
    @check('medicine_list')
    @swag_from('../swagger/medicine/list_medicine.yaml')
    def get(self):
        query = MedicineModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medicine_insert')
    @swag_from('../swagger/medicine/post_medicine.yaml')
    def post(self):
        data = Medicine.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicineModel.find_by_id(id):
            return {'message': _("MEDICINE_DUPLICATED").format(id)}, 400

        medicine = MedicineModel(**data)
        try:
            medicine.user_create = get_jwt_identity()
            medicine.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating medicine.', exc_info=e)
            return {"message": _("MEDICINE_CREATE_ERROR")}, 500

        return medicine.json(), 201


class MedicineSearch(Resource):

    @jwt_required()
    @check('medicine_search')
    @swag_from('../swagger/medicine/search_medicine.yaml')
    def post(self):
        query = MedicineModel.query

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            if 'stock_control_select' in filters and filters.get('stock_control_select'):
                query = query.filter(MedicineModel.stock_control == True)

            and_filter_list = restrict_collector(and_filter_list, filters, 'id', lambda x: MedicineModel.id == x)
            and_filter_list = restrict_collector(and_filter_list, filters, 'stock_control', lambda x: MedicineModel.stock_control == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'description', lambda x: func.lower(MedicineModel.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'code', lambda x: func.lower(MedicineModel.code).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'concentration', lambda x: func.lower(MedicineModel.concentration).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'pharmaceutical_form', lambda x: func.lower(MedicineModel.pharmaceutical_form).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'via_admin', lambda x: func.lower(MedicineModel.via_admin).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'presentation', lambda x: func.lower(MedicineModel.presentation).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_create', lambda x: func.to_char(MedicineModel.date_create, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_create', lambda x: func.lower(MedicineModel.user_create).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_modify', lambda x: func.to_char(MedicineModel.date_modify, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_modify', lambda x: func.lower(MedicineModel.user_modify).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'generic_name', lambda x: func.lower(MedicineModel.generic_name).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
