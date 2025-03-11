from db import db
from flasgger import swag_from
from flask import request
from flask_babel import _
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Helpers.resource_helper import ResourceHelper
from models.product import ProductModel
from models.treatment_scheme import TreatmentSchemeModel
from models.treatment_scheme_product import TreatmentSchemeProductModel
from models.user import UserModel
from security import check, check_hospital
from utils import paginated_results, restrict


class TreatmentScheme(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=ResourceHelper.validate_text_255, required=False)
    parser.add_argument('description', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('periodicity_id', type=ResourceHelper.validate_scheme_periodicity, required=False)
    parser.add_argument('series_count', type=int, required=False)
    parser.add_argument('pre_medication', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('medication', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('post_medication', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('category_id', type=ResourceHelper.validate_scheme_category, required=False)
    parser.add_argument('notes', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('administration_time', type=int, required=False)
    parser.add_argument('preparation_instructions', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('status', type=int, required=False, default=1)


    @jwt_required()
    @check('treatment_scheme_get')
    @swag_from('swagger/treatment_scheme/get_treatment_scheme.yaml')
    @check_hospital
    def get(self, uuid, hospital_id):
        treatment_scheme = TreatmentSchemeModel.get_by_uuid(uuid, hospital_id)
        if not treatment_scheme:
            return {"message": _('RECORD_NOT_FOUND')}, 400

        return treatment_scheme.json(jsondepth=request.args.get('jsondepth', 2, int))


    @jwt_required()
    @check('treatment_scheme_update')
    @swag_from('swagger/treatment_scheme/put_treatment_scheme.yaml')
    @check_hospital
    def put(self, uuid, hospital_id):
        return self.handle_data(hospital_id, uuid)


    @jwt_required()
    @check('treatment_scheme_delete')
    @swag_from('swagger/treatment_scheme/delete_treatment_scheme.yaml')
    @check_hospital
    def delete(self, uuid, hospital_id):
        treatment_scheme = TreatmentSchemeModel.get_by_uuid(uuid, hospital_id)
        if not treatment_scheme:
            return {"message": _('RECORD_NOT_FOUND')}, 400

        try:
            for scheme_product in treatment_scheme.scheme_products:
                db.session.delete(scheme_product)

            treatment_scheme.delete_from_db()

        except Exception as e:
            db.session.rollback()
            return {
                "message": _("PROCESS_ERROR"),
                # "error": str(e)
            }, 500

        return {'message': _('PROCESS_SUCCESS')}, 200

    @staticmethod
    def handle_data(hospital_id, uuid=None):
        is_update = uuid is not None
        user = UserModel.find_by_user(get_jwt_identity())

        if is_update:
            new_treatment_scheme = TreatmentSchemeModel.get_by_uuid(uuid, hospital_id)
            if not new_treatment_scheme:
                return {"message": _('RECORD_NOT_FOUND')}, 400

            TreatmentScheme.parser.replace_argument('name', type=ResourceHelper.validate_text_255, required=False)
            new_data = TreatmentScheme.parser.parse_args()
            new_name = new_data.get('name')
            if new_name and new_treatment_scheme.name != new_name and TreatmentSchemeModel.get_by_name(new_name, hospital_id).first():
                return {"message": _("ALREADY_EXISTS_ERROR")}, 400

            TreatmentSchemeModel.from_reqparse(new_treatment_scheme, new_data)

        else:
            TreatmentScheme.parser.replace_argument('name', type=ResourceHelper.validate_text_255, required=True, help=_('REQUIRED_FIELD'))
            new_data = TreatmentScheme.parser.parse_args()
            if TreatmentSchemeModel.get_by_name(new_data.get('name'), hospital_id):
                return {"message": {"name": _("ALREADY_EXISTS_ERROR")}}, 400

            new_treatment_scheme = TreatmentSchemeModel()
            new_treatment_scheme.hospital_id = hospital_id
            new_treatment_scheme.created_user_id = user.id

        TreatmentSchemeModel.from_reqparse(new_treatment_scheme, new_data)

        new_treatment_scheme.edited_user_id = user.id

        try:
            db.session.add(new_treatment_scheme)
            db.session.flush()

        except Exception as e:
            db.session.rollback()
            return {
                "message": _("PROCESS_ERROR"),
                # "error": str(e)
            }, 500

        result = TreatmentScheme.handle_products(is_update, new_treatment_scheme, user.id)
        if "message" in result:
            return result, 400

        db.session.commit()

        return {
            "message": _("PROCESS_SUCCESS"),
            "treatment_scheme": new_treatment_scheme.json()
        }, 200 if is_update else 201


    @staticmethod
    def handle_products(is_update, treatment_scheme, user_id, request_scheme=None):
        scheme_products_data = request.json.get('scheme_products', [])
        if not isinstance(scheme_products_data, list):
            return {"message": {"scheme_products": _('INVALID_TYPE')}}, 400

        _index = 0
        sch_prod_uuids = []
        is_request_scheme = request_scheme is not None
        for scheme_product in scheme_products_data:
            if is_update and 'uuid' in scheme_product:
                _uuid = scheme_product.get('uuid')
                _new_scheme_product = TreatmentSchemeProductModel.get_by_uuid(_uuid)
                if not _new_scheme_product or _new_scheme_product.treatment_scheme_id != treatment_scheme.id:
                    return {
                        "message": {
                            "scheme_product" : _("RECORD_NOT_FOUND") + ': ' + _uuid
                        }
                    }, 400

                sch_prod_uuids.append(_uuid)

            else:
                _new_scheme_product = TreatmentSchemeProductModel()
                _new_scheme_product.treatment_scheme_id = treatment_scheme.id
                _new_scheme_product.created_user_id = user_id

            base_scheme_products = {}
            if is_request_scheme:
                base_treatment_scheme_products = request_scheme.base_treatment_scheme.scheme_products
                base_scheme_products = {product.index: product for product in base_treatment_scheme_products}

                _product_id = base_scheme_products[_index].product_id
                _administration_route_id = base_scheme_products[_index].administration_route_id
                _calculation_type_id = base_scheme_products[_index].calculation_type_id
                _frequency_id = base_scheme_products[_index].frequency_id
                _note = base_scheme_products[_index].note
                _adjustable = base_scheme_products[_index].adjustable
                _status = base_scheme_products[_index].status

            else:
                _product_id = None
                _product_uuid = ResourceHelper.trim_string(scheme_product.get('product_uuid'))
                if _product_uuid:
                    _product = ProductModel.get_by_uuid(_product_uuid, treatment_scheme.hospital_id)
                    if _product:
                        _product_id = _product.id
                    else:
                        return {
                            "message": {
                                "product" : _("RECORD_NOT_FOUND") + ': ' + _product_uuid
                            }
                        }, 400
                    
                try:
                    _administration_route_id = scheme_product.get('administration_route_id')
                    if _administration_route_id:
                        _administration_route_id = ResourceHelper.validate_administration_route(_administration_route_id)
    
                except Exception as e:
                    db.session.rollback()
                    return {"message": {"administration_route_id": str(e)}}, 400
    
                try:
                    _calculation_type_id = scheme_product.get('calculation_type_id')
                    if _calculation_type_id:
                        _calculation_type_id = ResourceHelper.validate_calculation_type(_calculation_type_id)
    
                except Exception as e:
                    db.session.rollback()
                    return {"message": {"calculation_type_id": str(e)}}, 400
    
                try:
                    _frequency_id = scheme_product.get('frequency_id')
                    if _frequency_id:
                        _frequency_id = ResourceHelper.validate_frequency(_frequency_id)
    
                except Exception as e:
                    db.session.rollback()
                    return {"message": {"frequency_id": str(e)}}, 400
    
                _note = scheme_product.get('note').strip() if scheme_product.get('note') else None
                _adjustable = bool(scheme_product.get('adjustable'))
                _status = int(scheme_product.get('status', '1'))

            _loading_dose = float(scheme_product.get('loading_dose', '0'))
            _session_dose = float(scheme_product.get('session_dose', '0'))
            _infusion_dose = float(scheme_product.get('infusion_dose', '0'))
            _adjust_comment = scheme_product.get('adjust_comment').strip() if scheme_product.get('adjust_comment') else None

            try:
                if is_request_scheme:
                    _dose_changed = False
                    if is_update:
                        if (_loading_dose != _new_scheme_product.loading_dose or
                            _session_dose != _new_scheme_product.session_dose or
                            _infusion_dose != _new_scheme_product.infusion_dose):
                            _dose_changed = True
                    else:
                        if (_loading_dose != base_scheme_products[_index].loading_dose or
                                _session_dose != base_scheme_products[_index].session_dose or
                                _infusion_dose != base_scheme_products[_index].infusion_dose):
                            _dose_changed = True

                    if _dose_changed:
                        if not _adjustable:
                            db.session.rollback()
                            return {"message": {"adjust": _("DOSE_NOT_ADJUSTABLE")}}, 400

                        if not _adjust_comment:
                            db.session.rollback()
                            return {"message": {"adjust_comment": _("REQUIRED_FIELD")}}, 400

                        if is_update:
                            _new_scheme_product.status = 0
                            db.session.add(_new_scheme_product)

                            _changed_id = _new_scheme_product.id

                            _new_scheme_product = TreatmentSchemeProductModel()
                            _new_scheme_product.treatment_scheme_id = treatment_scheme.id
                            _new_scheme_product.created_user_id = user_id
                            _new_scheme_product.prev_treatment_scheme_product = _changed_id

                        _new_scheme_product.adjust_comment = _adjust_comment

                _new_scheme_product.product_id = _product_id
                _new_scheme_product.administration_route_id = _administration_route_id
                _new_scheme_product.calculation_type_id = _calculation_type_id
                _new_scheme_product.frequency_id = _frequency_id
                _new_scheme_product.note = _note
                _new_scheme_product.adjustable = _adjustable
                _new_scheme_product.status = _status
                _new_scheme_product.index = _index
                _new_scheme_product.edited_user_id = user_id
                _new_scheme_product.loading_dose = _loading_dose
                _new_scheme_product.session_dose = _session_dose
                _new_scheme_product.infusion_dose = _infusion_dose

                db.session.add(_new_scheme_product)

            except Exception as e:
                db.session.rollback()
                return {
                    "message": _("PROCESS_ERROR"),
                    # "error": str(e)
                }, 500

            _index += 1

        if is_update and not is_request_scheme:
            for scheme_product in treatment_scheme.scheme_products:
                if str(scheme_product.uuid) not in sch_prod_uuids:
                    db.session.delete(scheme_product)

        return {}


class TreatmentSchemeList(Resource):

    @jwt_required()
    @check('treatment_scheme_list')
    @swag_from('swagger/treatment_scheme/list_treatment_scheme.yaml')
    @check_hospital
    def get(self, hospital_id):
        query = TreatmentSchemeModel.query_find_all(hospital_id)
        return paginated_results(query, depth=2)


    @jwt_required()
    @check('treatment_scheme_insert')
    @swag_from('swagger/treatment_scheme/post_treatment_scheme.yaml')
    @check_hospital
    def post(self, hospital_id):
        return TreatmentScheme.handle_data(hospital_id)


class TreatmentSchemeSearch(Resource):

    @jwt_required()
    @check('treatment_scheme_list')
    @swag_from('swagger/treatment_scheme/search_treatment_scheme.yaml')
    @check_hospital
    def post(self, hospital_id):
        query = TreatmentSchemeModel.query_find_all(hospital_id)
        filters = request.json
        if filters:
            query = restrict(query, filters, 'name', lambda x: TreatmentSchemeModel.name.ilike(f"%{x}%"))
            query = restrict(query, filters, 'description', lambda x: TreatmentSchemeModel.description.ilike(f"%{x}%"))

        query = query.order_by(TreatmentSchemeModel.name.asc()).order_by(TreatmentSchemeModel.id.asc())
        return paginated_results(query)
