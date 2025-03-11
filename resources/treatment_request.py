from db import db
from flasgger import swag_from
from flask import request
from flask_babel import _
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Helpers.resource_helper import ResourceHelper
from models.treatment_request import TreatmentRequestModel
from models.treatment_request_scheme import TreatmentRequestSchemeModel
from models.treatment_scheme import TreatmentSchemeModel, TreatmentRequestTypeEnum
from models.user import UserModel
from resources.treatment_scheme import TreatmentScheme
from utils import paginated_results, restrict
from security import check, check_hospital


class TreatmentRequest(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('patient_id', type=ResourceHelper.validate_patient, required=False)
    parser.add_argument('protocol_id', type=ResourceHelper.validate_protocol, required=False)
    parser.add_argument('specialty_id', type=ResourceHelper.validate_specialty, required=False)
    parser.add_argument('stage_id', type=ResourceHelper.validate_cancer_stage, required=False)
    parser.add_argument('criteria_id', type=ResourceHelper.validate_request_criteria, required=False)
    parser.add_argument('date', type=ResourceHelper.validate_date, required=False)
    parser.add_argument('is_urgent', type=bool, required=False)
    parser.add_argument('status', type=int, required=False, default=1)
    parser.add_argument('comment', type=ResourceHelper.trim_string, required=False)
    parser.add_argument('patient_weight', type=float, required=False)
    parser.add_argument('patient_height', type=float, required=False)
    parser.add_argument('body_surface_area', type=float, required=False)

    parser.add_argument('diagnosis_id', type=ResourceHelper.validate_diagnosis, required=False)
    parser.add_argument('topography_id', type=ResourceHelper.validate_topography, required=False)
    parser.add_argument('morphology_id', type=ResourceHelper.validate_morphology, required=False)

    parser_scheme = reqparse.RequestParser()
    parser_scheme.add_argument('base_treatment_scheme_uuid', type=ResourceHelper.validate_treatment_scheme, required=True)
    parser_scheme.add_argument('name', type=ResourceHelper.validate_text_255, required=False)
    parser_scheme.add_argument('description', type=ResourceHelper.trim_string, required=False)
    parser_scheme.add_argument('periodicity_id', type=ResourceHelper.validate_scheme_periodicity, required=False)
    parser_scheme.add_argument('series_count', type=int, required=False)
    parser_scheme.add_argument('pre_medication', type=ResourceHelper.trim_string, required=False)
    parser_scheme.add_argument('medication', type=ResourceHelper.trim_string, required=False)
    parser_scheme.add_argument('post_medication', type=ResourceHelper.trim_string, required=False)
    parser_scheme.add_argument('notes', type=ResourceHelper.trim_string, required=False)
    parser_scheme.add_argument('administration_time', type=int, required=False)
    parser_scheme.add_argument('preparation_instructions', type=ResourceHelper.trim_string, required=False)


    @jwt_required()
    @check('treatment_request_get')
    @swag_from('swagger/treatment_request/get_treatment_request.yaml')
    @check_hospital
    def get(self, uuid, hospital_id):
        treatment_request = TreatmentRequestModel.get_by_uuid(uuid, hospital_id)
        if not treatment_request:
            return {"message": _('RECORD_NOT_FOUND')}, 400

        return treatment_request.json(jsondepth=request.args.get('jsondepth', 2, int))


    @jwt_required()
    @check('treatment_request_update')
    @swag_from('swagger/treatment_request/put_treatment_request.yaml')
    @check_hospital
    def put(self, uuid, hospital_id):
        return self.handle_data(hospital_id, uuid)


    @jwt_required()
    @check('treatment_request_delete')
    @swag_from('swagger/treatment_request/delete_treatment_request.yaml')
    @check_hospital
    def delete(self, uuid, hospital_id):
        treatment_request = TreatmentRequestModel.get_by_uuid(uuid, hospital_id)
        if not treatment_request:
            return {"message": _('RECORD_NOT_FOUND')}, 400

        try:
            treatment_request.delete_from_db()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": _("PROCESS_ERROR")}, 500

        return {"message": _("PROCESS_SUCCESS")}, 200


    @staticmethod
    def handle_data(hospital_id, uuid=None):
        is_update = uuid is not None
        user = UserModel.find_by_user(get_jwt_identity())
        parsed_data = TreatmentRequest.parser.parse_args()
        parsed_request_scheme_data = TreatmentRequest.parser_scheme.parse_args()
        parsed_scheme_data = TreatmentRequest.parser_scheme.parse_args()

        # TODO: calculate the "body_surface_area"

        if is_update:
            treatment_request = TreatmentRequestModel.get_by_uuid(uuid, hospital_id)
            if not treatment_request:
                return {"message": _('RECORD_NOT_FOUND')}, 400

            TreatmentRequestModel.from_reqparse(treatment_request, parsed_data)
            request_scheme = TreatmentRequestSchemeModel.get_current_for_request(treatment_request.id)
            treatment_scheme = request_scheme.treatment_scheme

        else:
            treatment_request = TreatmentRequestModel()
            treatment_request.hospital_id = hospital_id
            treatment_request.created_user_id = user.id
            TreatmentRequestModel.from_reqparse(treatment_request, parsed_data)

            request_scheme = TreatmentRequestSchemeModel()
            request_scheme.base_treatment_scheme_id = parsed_request_scheme_data.get('base_treatment_scheme_uuid')
            TreatmentRequestSchemeModel.from_reqparse(request_scheme, parsed_request_scheme_data)

            treatment_scheme = TreatmentSchemeModel()
            TreatmentSchemeModel.from_reqparse(treatment_scheme,parsed_scheme_data)
            treatment_scheme.hospital_id = hospital_id
            treatment_scheme.created_user_id = user.id
            treatment_scheme.type = TreatmentRequestTypeEnum.TREATMENT_REQUEST_SCHEMA.value

        treatment_request.edited_user_id = user.id
        treatment_scheme.edited_user_id = user.id

        try:
            db.session.add(treatment_request)

            db.session.add(treatment_scheme)

            db.session.flush()

            request_scheme.treatment_request_id = treatment_request.id
            request_scheme.treatment_scheme_id = treatment_scheme.id
            db.session.add(request_scheme)

        except Exception as e:
            db.session.rollback()
            return {"message": _("PROCESS_ERROR")}, 500

        result = TreatmentScheme.handle_products(is_update, treatment_scheme, user.id, request_scheme)
        if "message" in result:
            return result, 400

        db.session.commit()

        return {
            "message": _("PROCESS_SUCCESS"),
            "treatment_request": treatment_request.json()
        }, 200 if is_update else 201


class TreatmentRequestList(Resource):

    @jwt_required()
    @check('treatment_request_list')
    @swag_from('swagger/treatment_request/list_treatment_request.yaml')
    @check_hospital
    def get(self, hospital_id):
        query = TreatmentRequestModel.query_find_all(hospital_id)
        return paginated_results(query, depth=2)


    @jwt_required()
    @check('treatment_request_insert')
    @swag_from('swagger/treatment_request/post_treatment_request.yaml')
    @check_hospital
    def post(self, hospital_id):
        return TreatmentRequest.handle_data(hospital_id)


class TreatmentRequestSearch(Resource):

    @jwt_required()
    @check('treatment_request_list')
    @swag_from('swagger/treatment_request/search_treatment_request.yaml')
    @check_hospital
    def post(self, hospital_id):
        query = TreatmentRequestModel.query.filter_by(hospital_id=hospital_id)
        filters = request.json

        if filters:
            query = restrict(query, filters, 'comment', lambda x: TreatmentRequestModel.comment.ilike(f"%{x}%"))
            query = restrict(query, filters, 'is_urgent', lambda x: TreatmentRequestModel.is_urgent.is_(x))
            query = restrict(query, filters, 'date', lambda x: TreatmentRequestModel.date == x)

        query = query.order_by(TreatmentRequestModel.date.asc()).order_by(TreatmentRequestModel.id.asc())
        return paginated_results(query)
