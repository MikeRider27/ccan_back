import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask_babel import _
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import aliased

from models.deposit import DepositModel
from models.hospital import HospitalModel
from models.parameter import ParameterModel
from security import check
from utils import restrict, paginated_results, restrict_collector


class Deposit(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('code', type=str)
    parser.add_argument('type_id', type=int)
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('address', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('phone', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('origin', type=str)

    @jwt_required()
    @check('deposit_get')
    @swag_from('../swagger/deposit/get_deposit.yaml')
    def get(self, id):
        deposit = DepositModel.find_by_id(id)
        if deposit:
            return deposit.json()
        return {'message': _("DEPOSIT_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_update')
    @swag_from('../swagger/deposit/put_deposit.yaml')
    def put(self, id):
        deposit = DepositModel.find_by_id(id)
        if deposit:
            newdata = Deposit.parser.parse_args()
            DepositModel.from_reqparse(deposit, newdata)
            deposit.date_modify = datetime.now()
            deposit.user_modify = get_jwt_identity()
            deposit.save_to_db()
            return deposit.json()
        return {'message': _("DEPOSIT_NOT_FOUND")}, 404

    @jwt_required()
    @check('deposit_delete')
    @swag_from('../swagger/deposit/delete_deposit.yaml')
    def delete(self, id):
        deposit = DepositModel.find_by_id(id)
        if deposit:
            deposit.delete_from_db()

        return {'message': _("DEPOSIT_DELETED")}


class DepositList(Resource):

    @jwt_required()
    @check('deposit_list')
    @swag_from('../swagger/deposit/list_deposit.yaml')
    def get(self):
        query = DepositModel.query
        return paginated_results(query)

    @jwt_required()
    @check('deposit_insert')
    @swag_from('../swagger/deposit/post_deposit.yaml')
    def post(self):
        data = Deposit.parser.parse_args()

        id = data.get('id')

        if id is not None and DepositModel.find_by_id(id):
            return {'message': _("DEPOSIT_DUPLICATED").format(id)}, 400

        deposit = DepositModel(**data)
        try:
            deposit.date_create = datetime.now()
            deposit.user_create = get_jwt_identity()
            deposit.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating deposit.', exc_info=e)
            return {"message": _("DEPOSIT_CREATE_ERROR")}, 500

        return deposit.json(), 201


class DepositSearch(Resource):

    @jwt_required()
    @check('deposit_search')
    @swag_from('../swagger/deposit/search_deposit.yaml')
    def post(self):
        query = DepositModel.query

        hospital = aliased(HospitalModel)
        query = query.outerjoin(hospital, and_(hospital.id == DepositModel.hospital_id))
        tipo = aliased(ParameterModel)
        query = query.outerjoin(tipo, and_(tipo.id == DepositModel.type_id))

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            or_filter_list = restrict_collector(or_filter_list, filters, 'deposit_hospital',
                                                lambda x: func.lower(hospital.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'code',
                                                lambda x: func.lower(DepositModel.code).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'type',
                                                lambda x: func.lower(tipo.value).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'name',
                                                lambda x: func.lower(DepositModel.name).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'description',
                                                lambda x: func.lower(DepositModel.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'origin',
                                                lambda x: func.lower(DepositModel.origin).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
