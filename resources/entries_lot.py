import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.entries_lot import EntriesLotModel
from utils import restrict, paginated_results
from security import check


class EntriesLot(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('lot_id', type=int)
    parser.add_argument('entries_id', type=int)

    @jwt_required()
    @check('entries_lot_get')
    @swag_from('../swagger/entries_lot/get_entries_lot.yaml')
    def get(self, id):
        entries_lot = EntriesLotModel.find_by_id(id)
        if entries_lot:
            return entries_lot.json()
        return {'message': _("ENTRIES_LOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('entries_lot_update')
    @swag_from('../swagger/entries_lot/put_entries_lot.yaml')
    def put(self, id):
        entries_lot= EntriesLotModel.find_by_id(id)
        if entries_lot:
            newdata = EntriesLot.parser.parse_args()
            EntriesLotModel.from_reqparse(entries_lot, newdata)
            entries_lot.save_to_db()
            return entries_lot.json()
        return {'message': _("ENTRIES_LOT_NOT_FOUND")}, 404

    @jwt_required()
    @check('entries_lot_delete')
    @swag_from('../swagger/entries_lot/delete_entries_lot.yaml')
    def delete(self, id):
        entries_lot = EntriesLotModel.find_by_id(id)
        if entries_lot:
            entries_lot.delete_from_db()

        return {'message': _("ENTRIES_LOT_DELETED")}


class EntriesLotList(Resource):

    @jwt_required()
    @check('entries_lot_list')
    @swag_from('../swagger/entries_lot/list_entries_lot.yaml')
    def get(self):
        query = EntriesLotModel.query
        return paginated_results(query)

    @jwt_required()
    @check('entries_lot_insert')
    @swag_from('../swagger/entries_lot/post_entries_lot.yaml')
    def post(self):
        data = EntriesLot.parser.parse_args()

        id = data.get('id')

        if id is not None and EntriesLotModel.find_by_id(id):
            return {'message': _("ENTRIES_LOT_DUPLICATED").format(id)}, 400

        entries_lot = EntriesLotModel(**data)
        try:
            entries_lot.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating entries lot.', exc_info=e)
            return {"message": _("ENTRIES_LOT_CREATE_ERROR")}, 500

        return entries_lot.json(), 201


class EntriesLotSearch(Resource):

    @jwt_required()
    @check('entries_lot_search')
    @swag_from('../swagger/entries_lot/search_entries_lot.yaml')
    def post(self):
        query = EntriesLotModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: EntriesLotModel.id == x)
            query = restrict(query, filters, 'lot_id', lambda x: EntriesLotModel.lot_id == x)
            query = restrict(query, filters, 'entries_id', lambda x: EntriesLotModel.entries_id == x)
        return paginated_results(query)
