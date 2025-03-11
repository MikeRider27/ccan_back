import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.diagnosis import DiagnosisModel
from utils import restrict, paginated_results
from security import check


class Diagnosis(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('codification_type', type=str)
    parser.add_argument('cie_10_code_id', type=int)
    parser.add_argument('cie_o_morphology_id', type=int)
    parser.add_argument('cie_o_topography_id', type=int)
    parser.add_argument('cie_o_tumor_location_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('hospital_id', type=int)

    @jwt_required()
    @check('diagnosis_get')
    @swag_from('../swagger/diagnosis/get_diagnosis.yaml')
    def get(self, id):
        diagnosis = DiagnosisModel.find_by_id(id)
        if diagnosis:
            return diagnosis.json()
        return {'message':  _("DIAGNOSIS_NOT_FOUND")}, 404

    @jwt_required()
    @check('diagnosis_update')
    @swag_from('../swagger/diagnosis/put_diagnosis.yaml')
    def put(self, id):
        diagnosis = DiagnosisModel.find_by_id(id)
        if diagnosis:
            newdata = Diagnosis.parser.parse_args()
            DiagnosisModel.from_reqparse(diagnosis, newdata)
            # It is manually assigned because these values can be None
            diagnosis.cie_10_code_id = newdata['cie_10_code_id']
            diagnosis.cie_o_morphology_id = newdata['cie_o_morphology_id']
            diagnosis.cie_o_topography_id = newdata['cie_o_topography_id']
            diagnosis.cie_o_tumor_location_id = newdata['cie_o_tumor_location_id']
            diagnosis.save_to_db()
            return diagnosis.json()
        return {'message': _("DIAGNOSIS_NOT_FOUND")}, 404

    @jwt_required()
    @check('diagnosis_delete')
    @swag_from('../swagger/diagnosis/delete_diagnosis.yaml')
    def delete(self, id):
        diagnosis = DiagnosisModel.find_by_id(id)
        if diagnosis:
            diagnosis.delete_from_db()

        return {'message': _("DIAGNOSIS_DELETED")}


class DiagnosisList(Resource):

    @jwt_required()
    @check('diagnosis_list')
    @swag_from('../swagger/diagnosis/list_diagnosis.yaml')
    def get(self):
        query = DiagnosisModel.query
        return paginated_results(query)

    @jwt_required()
    @check('diagnosis_insert')
    @swag_from('../swagger/diagnosis/post_diagnosis.yaml')
    def post(self):
        data = Diagnosis.parser.parse_args()

        id = data.get('id')

        if id is not None and DiagnosisModel.find_by_id(id):
            return {'message': _("DIAGNOSIS_DUPLICATED").format(id)}, 400

        diagnosis = DiagnosisModel(**data)
        try:
            diagnosis.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating Diagnosis.', exc_info=e)
            return {"message": _("DIAGNOSIS_CREATE_ERROR")}, 500

        return diagnosis.json(), 201


class DiagnosisSearch(Resource):

    @jwt_required()
    @check('diagnosis_search')
    @swag_from('../swagger/diagnosis/search_diagnosis.yaml')
    def post(self):
        query = DiagnosisModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: DiagnosisModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: DiagnosisModel.patient_id == x)
            query = restrict(query, filters, 'codification_type', lambda x: DiagnosisModel.codification_type.contains(x))
            query = restrict(query, filters, 'birthdate', lambda x: func.to_char(DiagnosisModel.date, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'cie_10_code_id', lambda x: DiagnosisModel.cie_10_code_id == x)
            query = restrict(query, filters, 'cie_o_morpholoty_id', lambda x: DiagnosisModel.cie_o_morphology_id == x)
            query = restrict(query, filters, 'cie_o_topography_id', lambda x: DiagnosisModel.cie_o_topography_id == x)
            query = restrict(query, filters, 'cie_o_tumor_location_id', lambda x: DiagnosisModel.cie_o_tumor_location_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: DiagnosisModel.hospital_id == x)
        return paginated_results(query)
