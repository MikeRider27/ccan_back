import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask_babel import _

from models.supplier import SupplierModel
from security import check
from utils import restrict, paginated_results


class Supplier(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('name', type=str)
    parser.add_argument('county_id', type=int)
    parser.add_argument('address', type=str)
    parser.add_argument('phone', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('state_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)

    @jwt_required()
    @check('supplier_get')
    @swag_from('../swagger/supplier/get_supplier.yaml')
    def get(self, id):
        supplier = SupplierModel.find_by_id(id)
        if supplier:
            return supplier.json()
        return {'message': _("SUPPLIER_NOT_FOUND")}, 404

    @jwt_required()
    @check('supplier_update')
    @swag_from('../swagger/supplier/put_supplier.yaml')
    def put(self, id):
        supplier = SupplierModel.find_by_id(id)
        if supplier:
            newdata = Supplier.parser.parse_args()
            SupplierModel.from_reqparse(supplier, newdata)
            supplier.date_modify = datetime.now()
            supplier.user_modify = get_jwt_identity()
            supplier.save_to_db()
            return supplier.json()
        return {'message': _("SUPPLIER_NOT_FOUND")}, 404

    @jwt_required()
    @check('supplier_delete')
    @swag_from('../swagger/supplier/delete_supplier.yaml')
    def delete(self, id):
        supplier = SupplierModel.find_by_id(id)
        if supplier:
            supplier.delete_from_db()

        return {'message': _("SUPPLIER_DELETED")}


class SupplierList(Resource):

    @jwt_required()
    @check('supplier_list')
    @swag_from('../swagger/supplier/list_supplier.yaml')
    def get(self):
        query = SupplierModel.query
        return paginated_results(query)

    @jwt_required()
    @check('supplier_insert')
    @swag_from('../swagger/supplier/post_supplier.yaml')
    def post(self):
        data = Supplier.parser.parse_args()

        id = data.get('id')

        if id is not None and SupplierModel.find_by_id(id):
            return {'message': _("SUPPLIER_DUPLICATED").format(id)}, 400

        supplier = SupplierModel(**data)
        try:
            supplier.date_create = datetime.now()
            supplier.user_create = get_jwt_identity()
            supplier.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating supplier', exc_info=e)
            return {"message": _("SUPPLIER_CREATE_ERROR")}, 500

        return supplier.json(), 201


class SupplierSearch(Resource):

    @jwt_required()
    @check('supplier_search')
    @swag_from('../swagger/supplier/search_supplier.yaml')
    def post(self):
        query = SupplierModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: SupplierModel.id == x)
            query = restrict(query, filters, 'name', lambda x: SupplierModel.name.contains(x))
            query = restrict(query, filters, 'county_id', lambda x: SupplierModel.county_id == x)
            query = restrict(query, filters, 'address', lambda x: SupplierModel.address.contains(x))
            query = restrict(query, filters, 'phone', lambda x: SupplierModel.phone.contains(x))
            query = restrict(query, filters, 'email', lambda x: SupplierModel.email.contains(x))
            query = restrict(query, filters, 'description', lambda x: SupplierModel.description.contains(x))
            query = restrict(query, filters, 'state_id', lambda x: SupplierModel.state_id == x)
            query = restrict(query, filters, 'user_create', lambda x: SupplierModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: SupplierModel.user_modify.contains(x))
        return paginated_results(query)
