import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask_babel import _

from models.manufacturer import ManufacturerModel
from security import check
from utils import restrict, paginated_results


class Manufacturer(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('name', type=str)
    parser.add_argument('county_id', type=int)
    parser.add_argument('state_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('manufacturer_get')
    @swag_from('../swagger/manufacturer/get_manufacturer.yaml')
    def get(self, id):
        manufacturer = ManufacturerModel.find_by_id(id)
        if manufacturer:
            return manufacturer.json()
        return {'message': _("MANUFACTURER_NOT_FOUND")}, 404

    @jwt_required()
    @check('manufacturer_update')
    @swag_from('../swagger/manufacturer/put_manufacturer.yaml')
    def put(self, id):
        manufacturer = ManufacturerModel.find_by_id(id)
        if manufacturer:
            newdata = Manufacturer.parser.parse_args()
            ManufacturerModel.from_reqparse(manufacturer, newdata)
            manufacturer.date_modify = datetime.now()
            manufacturer.user_modify = get_jwt_identity()
            manufacturer.save_to_db()
            return manufacturer.json()
        return {'message': _("MANUFACTURER_NOT_FOUND")}, 404

    @jwt_required()
    @check('manufacturer_delete')
    @swag_from('../swagger/manufacturer/delete_manufacturer.yaml')
    def delete(self, id):
        manufacturer = ManufacturerModel.find_by_id(id)
        if manufacturer:
            manufacturer.delete_from_db()

        return {'message': _("MANUFACTURER_DELETED")}


class ManufacturerList(Resource):

    @jwt_required()
    @check('manufacturer_list')
    @swag_from('../swagger/manufacturer/list_manufacturer.yaml')
    def get(self):
        query = ManufacturerModel.query
        return paginated_results(query)

    @jwt_required()
    @check('manufacturer_insert')
    @swag_from('../swagger/manufacturer/post_manufacturer.yaml')
    def post(self):
        data = Manufacturer.parser.parse_args()

        id = data.get('id')

        if id is not None and ManufacturerModel.find_by_id(id):
            return {'message': _("MANUFACTURER_DUPLICATED").format(id)}, 400

        manufacturer = ManufacturerModel(**data)
        try:
            manufacturer.date_create = datetime.now()
            manufacturer.user_create = get_jwt_identity()
            manufacturer.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating manufacturer.', exc_info=e)
            return {"message": _("MANUFACTURER_CREATE_ERROR")}, 500

        return manufacturer.json(), 201


class ManufacturerSearch(Resource):

    @jwt_required()
    @check('manufacturer_search')
    @swag_from('../swagger/manufacturer/search_manufacturer.yaml')
    def post(self):
        query = ManufacturerModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: ManufacturerModel.id == x)
            query = restrict(query, filters, 'name', lambda x: ManufacturerModel.name.contains(x))
            query = restrict(query, filters, 'county_id', lambda x: ManufacturerModel.county_id == x)
            query = restrict(query, filters, 'state_id', lambda x: ManufacturerModel.state_id == x)
            query = restrict(query, filters, 'user_create', lambda x: ManufacturerModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: ManufacturerModel.user_modify.contains(x))
        return paginated_results(query)
