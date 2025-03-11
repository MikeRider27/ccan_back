import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.medicine_medical_consultation import MedicineMedicalConsultationModel
from utils import restrict, paginated_results
from security import check


class MedicineMedicalConsultation(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('medical_consultation_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('observation', type=str)
    parser.add_argument('dose', type=float)
    parser.add_argument('presentation', type=str)
    parser.add_argument('concentration', type=str)

    @jwt_required()
    @check('medicine_medical_consultation_get')
    @swag_from('../swagger/medicine_medical_consultation/get_medicine_medical_consultation.yaml')
    def get(self, id):
        medicine_medical_consultation = MedicineMedicalConsultationModel.find_by_id(id)
        if medicine_medical_consultation:
            return medicine_medical_consultation.json()
        return {'message': _("MEDICINE_MEDICAL_CONSULTATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_medical_consultation_update')
    @swag_from('../swagger/medicine_medical_consultation/put_medicine_medical_consultation.yaml')
    def put(self, id):
        medicine_medical_consultation = MedicineMedicalConsultationModel.find_by_id(id)
        if medicine_medical_consultation:
            newdata = MedicineMedicalConsultation.parser.parse_args()
            MedicineMedicalConsultationModel.from_reqparse(medicine_medical_consultation, newdata)
            medicine_medical_consultation.save_to_db()
            return medicine_medical_consultation.json()
        return {'message': _("MEDICINE_MEDICAL_CONSULTATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_medical_consultation_delete')
    @swag_from('../swagger/medicine_medical_consultation/delete_medicine_medical_consultation.yaml')
    def delete(self, id):
        medicine_medical_consultation = MedicineMedicalConsultationModel.find_by_id(id)
        if medicine_medical_consultation:
            medicine_medical_consultation.delete_from_db()

        return {'message': _("MEDICINE_MEDICAL_CONSULTATION_DELETED")}


class MedicineMedicalConsultationList(Resource):

    @jwt_required()
    @check('medicine_medical_consultation_list')
    @swag_from('../swagger/medicine_medical_consultation/list_medicine_medical_consultation.yaml')
    def get(self):
        query = MedicineMedicalConsultationModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medicine_medical_consultation_insert')
    @swag_from('../swagger/medicine_medical_consultation/post_medicine_medical_consultation.yaml')
    def post(self):
        data = MedicineMedicalConsultation.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicineMedicalConsultationModel.find_by_id(id):
            return {'message': _("MEDICINE_MEDICAL_CONSULTATION_DUPLICATED").format(id)}, 400

        medicine_medical_consultation = MedicineMedicalConsultationModel(**data)
        try:
            medicine_medical_consultation.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating medicine medical consultation.', exc_info=e)
            return {"message": _("MEDICINE_MEDICAL_CONSULTATION_CREATE_ERROR")}, 500

        return medicine_medical_consultation.json(), 201


class MedicineMedicalConsultationSearch(Resource):

    @jwt_required()
    @check('medicine_medical_consultation_search')
    @swag_from('../swagger/medicine_medical_consultation/search_medicine_medical_consultation.yaml')
    def post(self):
        query = MedicineMedicalConsultationModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MedicineMedicalConsultationModel.id == x)
            query = restrict(query, filters, 'medicine_id', lambda x: MedicineMedicalConsultationModel.medicine_id == x)
            query = restrict(query, filters, 'medical_consultation_id', lambda x: MedicineMedicalConsultationModel.medical_consultation_id == x)
            query = restrict(query, filters, 'observation', lambda x: MedicineMedicalConsultationModel.observation.contains(x))
            query = restrict(query, filters, 'presentation', lambda x: MedicineMedicalConsultationModel.presentation.contains(x))
            query = restrict(query, filters, 'concentration', lambda x: MedicineMedicalConsultationModel.concentration.contains(x))

        # default order
        query = query.order_by(MedicineMedicalConsultationModel.id.desc())
        return paginated_results(query)
