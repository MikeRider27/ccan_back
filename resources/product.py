from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_babel import _
from Helpers.resource_helper import ResourceHelper
from models.product import ProductModel
from models.user import UserModel
from security import check, check_hospital
from utils import paginated_results, restrict


class ProductResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('medicine_id', type=ResourceHelper.validate_medicine, required=False)
    parser.add_argument('drug_id', type=ResourceHelper.validate_drug_uuid, required=False)
    parser.add_argument('code', type=ResourceHelper.validate_text_15, required=False)
    parser.add_argument('description', type=ResourceHelper.validate_text_255, required=False)
    parser.add_argument('concentration', type=float, required=False)
    parser.add_argument('concentration_unit_id', type=ResourceHelper.validate_concentration_unit, required=False)
    parser.add_argument('quantity', type=float, required=False)
    parser.add_argument('quantity_unit_id', type=ResourceHelper.validate_quantity_unit, required=False)
    parser.add_argument('type_id', type=ResourceHelper.validate_product_type, required=False)
    parser.add_argument('status', type=int, required=False, default=1)
    parser.add_argument('premedication', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('medication', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('postmedication', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('dose_limit', type=float, required=False)
    parser.add_argument('dose_unit_id', type=ResourceHelper.validate_dose_unit, required=False)
    parser.add_argument('contraindications', type=ResourceHelper.trim_string, required=False)

    @jwt_required()
    @check('product_get')
    @swag_from('swagger/product/get_product.yaml')
    @check_hospital
    def get(self, uuid, hospital_id):
        product = ProductModel.get_by_uuid(uuid, hospital_id)
        if not product:
            return {'message': _('RECORD_NOT_FOUND')}, 400

        return product.json(jsondepth=request.args.get('jsondepth', 0, int))

    @jwt_required()
    @check('product_update')
    @swag_from('swagger/product/put_product.yaml')
    @check_hospital
    def put(self, uuid, hospital_id):
        product = ProductModel.get_by_uuid(uuid, hospital_id)
        if not product:
            return {'message': _('RECORD_NOT_FOUND')}, 400

        self.parser.replace_argument('code', type=ResourceHelper.validate_text_255, required=False)
        new_data = self.parser.parse_args()

        ProductModel.from_reqparse(product, new_data)

        user = UserModel.find_by_user(get_jwt_identity())
        product.edited_user_id = user.id

        product.save_to_db()

        return {'message': _('PROCESS_SUCCESS'), 'product': product.json()}, 200


    @jwt_required()
    @check('product_delete')
    @swag_from('swagger/product/delete_product.yaml')
    @check_hospital
    def delete(self, uuid, hospital_id):
        product = ProductModel.get_by_uuid(uuid, hospital_id)
        if not product:
            return {'message': _('RECORD_NOT_FOUND')}, 400

        product.delete_from_db()

        return {'message': _('PROCESS_SUCCESS')}, 200


class ProductListResource(Resource):
    @jwt_required()
    @check('product_list')
    @swag_from('swagger/product/list_product.yaml')
    @check_hospital
    def get(self, hospital_id):
        products = ProductModel.query_find_all(hospital_id)
        return paginated_results(products)


    @jwt_required()
    @check('product_insert')
    @swag_from('swagger/product/post_product.yaml')
    @check_hospital
    def post(self, hospital_id):
        # here since the _() is now configured (won't be at class load)
        ProductResource.parser.replace_argument('code', type=ResourceHelper.trim_string, required=True, help=_('REQUIRED_FIELD'))

        data = ProductResource.parser.parse_args()

        if ProductModel.exists_by_hospital_and_code(hospital_id, data.get('code')):
            return {'message': _('CODE_ALREADY_EXISTS')}, 400

        user = UserModel.find_by_user(get_jwt_identity())

        new_product = ProductModel()
        ProductModel.from_reqparse(new_product, data)

        new_product.hospital_id = hospital_id
        new_product.created_user_id = user.id
        new_product.edited_user_id = user.id

        try:
            new_product.save_to_db()
            return {'message': _('PROCESS_SUCCESS'), 'product': new_product.json()}, 201

        except Exception as e:
            # return {'message': _('PROCESS_ERROR'), 'error': str(e)}, 500
            return {'message': _('PROCESS_ERROR'), 'error': 'Error general'}, 500


class ProductSearchResource(Resource):

    @jwt_required()
    @check('product_search')
    @swag_from('swagger/product/search_product.yaml')
    @check_hospital
    def post(self, hospital_id):
        query = ProductModel.query.filter_by(hospital_id=hospital_id)
        filters = request.json
        if filters:
            query = restrict(query, filters, 'medicine_id', lambda x: ProductModel.medicine_id == x)
            query = restrict(query, filters, 'drug_id', lambda x: ProductModel.drug_id == x)
            query = restrict(query, filters, 'code', lambda x: ProductModel.code.ilike(f'%{x}%'))
            query = restrict(query, filters, 'description', lambda x: ProductModel.description.ilike(f'%{x}%'))
            query = restrict(query, filters, 'type_id', lambda x: ProductModel.type_id == x)
            query = restrict(query, filters, 'status', lambda x: ProductModel.status == x)
            query = restrict(query, filters, 'premedication', lambda x: ProductModel.premedication.ilike(f'%{x}%'))
            query = restrict(query, filters, 'medication', lambda x: ProductModel.medication.ilike(f'%{x}%'))
            query = restrict(query, filters, 'postmedication', lambda x: ProductModel.postmedication.ilike(f'%{x}%'))
            query = restrict(query, filters, 'contraindications', lambda x: ProductModel.contraindications.ilike(f'%{x}%'))

        query = query.order_by(ProductModel.code.asc(), ProductModel.id.asc())
        return paginated_results(query)
