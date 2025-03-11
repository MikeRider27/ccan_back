import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func
from flask_babel import _

from models.diagnosis_ap import DiagnosisApModel
from utils import restrict, paginated_results
from security import check


class DiagnosisAp(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('observation', type=str)
    parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('tumor_size', type=float)
    parser.add_argument('cie_o_morphology_id', type=int)
    parser.add_argument('cie_o_topography_id', type=int)
    parser.add_argument('cie_o_tumor_location_id', type=int)
    parser.add_argument('armpit_node_number', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('doctor_id', type=int)
    parser.add_argument('armpit', type=str)
    parser.add_argument('re', type=str)
    parser.add_argument('rp', type=str)
    parser.add_argument('her2', type=str)
    parser.add_argument('her2_positive_id', type=int)
    parser.add_argument('general_report', type=str)
    parser.add_argument('origin', type=str)
    parser.add_argument('dx_presuntivo', type=str)
    parser.add_argument('material', type=str)
    parser.add_argument('diagnostico', type=str)
    parser.add_argument('clasificacion', type=str)
    parser.add_argument('macroscopia', type=str)
    parser.add_argument('microscopia', type=str)

    @jwt_required()
    @check('diagnosis_ap_get')
    @swag_from('../swagger/diagnosis_ap/get_diagnosis_ap.yaml')
    def get(self, id):
        diagnosis_ap = DiagnosisApModel.find_by_id(id)
        if diagnosis_ap:
            return diagnosis_ap.json()
        return {'message': _("DIAGNOSIS_AP_NOT_FOUND")}, 404

    @jwt_required()
    @check('diagnosis_ap_update')
    @swag_from('../swagger/diagnosis_ap/put_diagnosis_ap.yaml')
    def put(self, id):
        diagnosis_ap = DiagnosisApModel.find_by_id(id)
        if diagnosis_ap:
            newdata = DiagnosisAp.parser.parse_args()
            DiagnosisApModel.from_reqparse(diagnosis_ap, newdata)

            diagnosis_ap.user_modify = get_jwt_identity()
            diagnosis_ap.date_modify = datetime.now()
            diagnosis_ap.save_to_db()
            return diagnosis_ap.json()
        return {'message': _("DIAGNOSIS_AP_NOT_FOUND")}, 404

    @jwt_required()
    @check('diagnosis_ap_delete')
    @swag_from('../swagger/diagnosis_ap/delete_diagnosis_ap.yaml')
    def delete(self, id):
        diagnosis_ap = DiagnosisApModel.find_by_id(id)
        if diagnosis_ap:
            diagnosis_ap.delete_from_db()

        return {'message': _("DIAGNOSIS_AP_DELETED")}


class DiagnosisApList(Resource):

    @jwt_required()
    @check('diagnosis_ap_list')
    @swag_from('../swagger/diagnosis_ap/list_diagnosis_ap.yaml')
    def get(self):
        query = DiagnosisApModel.query
        return paginated_results(query)

    @jwt_required()
    @check('diagnosis_ap_insert')
    @swag_from('../swagger/diagnosis_ap/post_diagnosis_ap.yaml')
    def post(self):
        data = DiagnosisAp.parser.parse_args()

        id = data.get('id')

        if id is not None and DiagnosisApModel.find_by_id(id):
            return {'message': _("DIAGNOSIS_AP_DUPLICATED").format(id)}, 400

        diagnosis_ap = DiagnosisApModel(**data)
        try:
            diagnosis_ap.user_create = get_jwt_identity()
            diagnosis_ap.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating Diagnosis AP.', exc_info=e)
            return {"message": _("DIAGNOSIS_AP_CREATE_ERROR")}, 500

        return diagnosis_ap.json(), 201


class DiagnosisApSearch(Resource):

    @jwt_required()
    @check('diagnosis_ap_search')
    @swag_from('../swagger/diagnosis_ap/search_diagnosis_ap.yaml')
    def post(self):
        query = DiagnosisApModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: DiagnosisApModel.id == x)
            query = restrict(query, filters, 'observation', lambda x: DiagnosisApModel.observation.contains(x))
            query = restrict(query, filters, 'tumor_size', lambda x: DiagnosisApModel.tumor_size == x)
            query = restrict(query, filters, 'cie_o_morphology_id',
                             lambda x: DiagnosisApModel.cie_o_morphology_id == x)
            query = restrict(query, filters, 'cie_o_topography_id',
                             lambda x: DiagnosisApModel.cie_o_topography_id == x)
            query = restrict(query, filters, 'cie_o_tumor_location_id',
                             lambda x: DiagnosisApModel.cie_o_tumor_location_id == x)
            query = restrict(query, filters, 'armpit_negative', lambda x: x)
            query = restrict(query, filters, 'armpit_positive', lambda x: x)
            query = restrict(query, filters, 'armpit_no_data', lambda x: x)
            query = restrict(query, filters, 'armpit_node_number', lambda x: DiagnosisApModel.armpit_node_number == x)
            query = restrict(query, filters, 'patient_id', lambda x: DiagnosisApModel.patient_id == x)
            query = restrict(query, filters, 'hospital_id', lambda x: DiagnosisApModel.hospital_id == x)
            query = restrict(query, filters, 'date_create',
                             lambda x: func.to_char(DiagnosisApModel.date_create, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_create', lambda x: DiagnosisApModel.user_create.contains(x))
            query = restrict(query, filters, 'date_modify',
                             lambda x: func.to_char(DiagnosisApModel.date_modify, 'DD/MM/YYYY').contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: DiagnosisApModel.user_modify.contains(x))
            query = restrict(query, filters, 'doctor_id', lambda x: DiagnosisApModel.doctor_id == x)
            query = restrict(query, filters, 'armpit', lambda x: DiagnosisApModel.re.contains(x))
            query = restrict(query, filters, 're', lambda x: DiagnosisApModel.re.contains(x))
            query = restrict(query, filters, 'rp', lambda x: DiagnosisApModel.rp.contains(x))
            query = restrict(query, filters, 'her2', lambda x: DiagnosisApModel.her2.contains(x))
            query = restrict(query, filters, 'her2_positive_id', lambda x: DiagnosisApModel.her2_positive_id == x)
            query = restrict(query, filters, 'general_report', lambda x: DiagnosisApModel.observation.contains(x))
            query = restrict(query, filters, 'origin', lambda x: DiagnosisApModel.origin.contains(x))
            query = restrict(query, filters, 'dx_presuntivo', lambda x: DiagnosisApModel.dx_presuntivo.contains(x))
            query = restrict(query, filters, 'material', lambda x: DiagnosisApModel.material.contains(x))
            query = restrict(query, filters, 'diagnostico', lambda x: DiagnosisApModel.diagnostico.contains(x))
            query = restrict(query, filters, 'clasificacion', lambda x: DiagnosisApModel.clasificacion.contains(x))
            query = restrict(query, filters, 'macroscopia', lambda x: DiagnosisApModel.macroscopia.contains(x))
            query = restrict(query, filters, 'microscopia', lambda x: DiagnosisApModel.microscopia.contains(x))

        # default order
        query = query.order_by(DiagnosisApModel.id.desc())

        return paginated_results(query)
