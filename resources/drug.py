from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_babel import _
from Helpers.resource_helper import ResourceHelper
from models.drug import DrugModel
from models.user import UserModel
from security import check
from utils import paginated_results, restrict


class DrugResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('generic_name', type=ResourceHelper.validate_text_255, required=False)
    parser.add_argument('therapeutic_action', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('category_id', type=ResourceHelper.validate_drug_category, required=False)
    parser.add_argument('status', type=int, required=False, default=1)


    @jwt_required()
    @check('drug_get')
    @swag_from('../swagger/drug/get_drug.yaml')
    def get(self, uuid):
        drug = DrugModel.get_by_uuid(uuid)
        if not drug:
            return {'message': _('RECORD_NOT_FOUND')}, 400

        return drug.json(jsondepth=request.args.get('jsondepth', 0, int))


    @jwt_required()
    @check('drug_update')
    @swag_from('../swagger/drug/put_drug.yaml')
    def put(self, uuid):
        drug = DrugModel.get_by_uuid(uuid)
        if not drug:
            return {'message': _('RECORD_NOT_FOUND')}, 400

        self.parser.replace_argument('generic_name', type=ResourceHelper.validate_text_255, required=False)
        new_data = self.parser.parse_args()
        DrugModel.from_reqparse(drug, new_data)

        user = UserModel.find_by_user(get_jwt_identity())
        drug.edited_user_id = user.id

        try:
            drug.save_to_db()
            return {'message': _('PROCESS_SUCCESS'), 'drug': drug.json()}, 200

        except Exception as e:
            # return {'message': _('PROCESS_ERROR'), 'error': str(e)}, 500
            return {'message': _('PROCESS_ERROR'), 'error': 'Error general'}, 500


    @jwt_required()
    @check('drug_delete')
    @swag_from('../swagger/drug/delete_drug.yaml')
    def delete(self, uuid):
        drug = DrugModel.get_by_uuid(uuid)
        if not drug:
            return {'message': _('RECORD_NOT_FOUND')}, 400

        try:
            drug.delete_from_db()
            return {'message': _('PROCESS_SUCCESS')}, 200

        except Exception as e:
            # return {'message': _('PROCESS_ERROR'), 'error': str(e)}, 500
            return {'message': _('PROCESS_ERROR'), 'error': 'Error general'}, 500



class DrugListResource(Resource):
    @jwt_required()
    @check('drug_list')
    @swag_from('../swagger/drug/list_drug.yaml')
    def get(self):
        drugs = DrugModel.query_find_all()
        return paginated_results(drugs)


    @jwt_required()
    @check('drug_insert')
    @swag_from('../swagger/drug/post_drug.yaml')
    def post(self):
        # here since the _() is now configured (won't be at class load)
        DrugResource.parser.replace_argument('generic_name', type=ResourceHelper.validate_text_255, required=True, help=_('REQUIRED_FIELD'))

        data = DrugResource.parser.parse_args()

        if DrugModel.query.filter_by(generic_name=data.get('generic_name')).first():
            return {'message': {'generic_name': _('ALREADY_EXISTS_ERROR')}}, 400

        user = UserModel.find_by_user(get_jwt_identity())

        new_drug = DrugModel()
        DrugModel.from_reqparse(new_drug, data)

        new_drug.created_user_id = user.id
        new_drug.edited_user_id = user.id

        try:
            new_drug.save_to_db()
            return {'message': _('PROCESS_SUCCESS'), 'drug': new_drug.json()}, 201

        except Exception as e:
            # return {'message': _('PROCESS_ERROR'), 'error': str(e)}, 500
            return {'message': _('PROCESS_ERROR'), 'error': 'Error general'}, 500


class DrugSearchResource(Resource):

    @jwt_required()
    @check('drug_search')
    @swag_from('../swagger/drug/search_drug.yaml')
    def post(self):
        query = DrugModel.query
        filters = request.json
        if filters:
            query = restrict(query, filters, 'generic_name', lambda x: DrugModel.generic_name.ilike(f'%{x}%'))
            query = restrict(query, filters, 'therapeutic_action', lambda x: DrugModel.therapeutic_action.ilike(f'%{x}%'))
            query = restrict(query, filters, 'category_id', lambda x: DrugModel.category_id == x)
            query = restrict(query, filters, 'status', lambda x: DrugModel.status == x)

        query = query.order_by(DrugModel.generic_name.asc(), DrugModel.id.asc())
        return paginated_results(query)
