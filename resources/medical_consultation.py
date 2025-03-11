import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import func, and_, or_
from flask_babel import _
from sqlalchemy.orm import aliased

from models.dispatch_medications import DispatchMedicationsModel
from models.doctor import DoctorModel
from models.hospital import HospitalModel
from models.medical_consultation import MedicalConsultationModel
from models.medicine_medical_consultation import MedicineMedicalConsultationModel
from models.patient import PatientModel
from utils import restrict, paginated_results, restrict_collector
from security import check


class MedicalConsultation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('date_first_diagnosis', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('diagnosis_by_id', type=int)
    parser.add_argument('observation', type=str)
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S'))
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S'))
    parser.add_argument('user_modify', type=str)
    parser.add_argument('date_consultation', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('cie_10_id', type=int)
    parser.add_argument('responsible_doctor_id', type=int)
    parser.add_argument('apply_chemotherapy', type=str)
    parser.add_argument('medicine_list', type=list, location='json')
    parser.add_argument('hospital_id', type=int)
    parser.add_argument('origin', type=str)

    @jwt_required()
    @check('medical_consultation_get')
    @swag_from('../swagger/medical_consultation/get_medical_consultation.yaml')
    def get(self, id):
        medical_consultation = MedicalConsultationModel.find_by_id(id)
        if medical_consultation:
            return medical_consultation.json()
        return {'message': _("MEDICAL_CONSULTATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_consultation_update')
    @swag_from('../swagger/medical_consultation/put_medical_consultation.yaml')
    def put(self, id):
        medical_consultation = MedicalConsultationModel.find_by_id(id)
        if medical_consultation:
            newdata = MedicalConsultation.parser.parse_args()
            medicine_medical_consultation_data_list = newdata['medicine_list']
            MedicalConsultationModel.from_reqparse(medical_consultation, newdata)

            # medicine_medical_consultation update
            medicine_medical_consultation_plan_list = []
            for medicine_medical_consultation_data in medicine_medical_consultation_data_list:
                del medicine_medical_consultation_data['medicine']
                data_id = medicine_medical_consultation_data.get('id', None)
                if data_id:
                    medicine_medical_consultation_model = MedicineMedicalConsultationModel.find_by_id(data_id)
                    MedicineMedicalConsultationModel.from_reqparse(medicine_medical_consultation_model,
                                                                   medicine_medical_consultation_data)
                else:
                    medicine_medical_consultation_model = MedicineMedicalConsultationModel(
                        **medicine_medical_consultation_data)
                medicine_medical_consultation_plan_list.append(medicine_medical_consultation_model)

            medical_consultation.medicine_list = medicine_medical_consultation_plan_list

            medical_consultation.user_modify = get_jwt_identity()
            medical_consultation.date_modify = datetime.now()
            medical_consultation.save_to_db()
            return medical_consultation.json()
        return {'message': _("MEDICAL_CONSULTATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_consultation_delete')
    @swag_from('../swagger/medical_consultation/delete_medical_consultation.yaml')
    def delete(self, id):
        medical_consultation = MedicalConsultationModel.find_by_id(id)
        if medical_consultation:
            medical_consultation.delete_from_db()

        return {'message': _("MEDICAL_CONSULTATION_DELETED")}


class MedicalConsultationList(Resource):

    @jwt_required()
    @check('medical_consultation_list')
    @swag_from('../swagger/medical_consultation/list_medical_consultation.yaml')
    def get(self):
        query = MedicalConsultationModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medical_consultation_insert')
    @swag_from('../swagger/medical_consultation/post_medical_consultation.yaml')
    def post(self):
        data = MedicalConsultation.parser.parse_args()

        id = data.get('id')
        if id is not None and MedicalConsultationModel.find_by_id(id):
            return {'message': _("MEDICAL_CONSULTATION_DUPLICATED").format(id)}, 400

        # Se extrae la fecha de la consulta
        consultation_date = data.get('date_consultation')

        # Se busca si ya existe una consulta en esa fecha
        existing_consultation = MedicalConsultationModel.query.filter_by(date_consultation=consultation_date).first()

        medicine_medical_consultation_data_list = data['medicine_list']
        del data['medicine_list']

        # Si ya existe se utiliza el id de la consulta existente, sino se crea una consulta
        if existing_consultation:
            medical_consultation = existing_consultation
        else:
            medical_consultation = MedicalConsultationModel(**data)
            try:
                medical_consultation.user_create = get_jwt_identity()
                medical_consultation.save_to_db()
            except Exception as e:
                logging.error('An error occurred while creating medical consultation.', exc_info=e)
                return {"message": _("MEDICAL_CONSULTATION_CREATE_ERROR")}, 500

        for medicine_medical_consultation_data in medicine_medical_consultation_data_list:
            if medicine_medical_consultation_data.get('medicine_id'):
                if 'medicine' in medicine_medical_consultation_data:
                    del medicine_medical_consultation_data['medicine']
                medicine_medical_consultation_data['medical_consultation_id'] = medical_consultation.id
                medicine_medical_consultation_model = MedicineMedicalConsultationModel(
                    **medicine_medical_consultation_data)
                medicine_medical_consultation_model.save_to_db()

        return medical_consultation.json(), 201

class MedicalConsultationSearch(Resource):

    @jwt_required()
    @check('medical_consultation_search')
    @swag_from('../swagger/medical_consultation/search_medical_consultation.yaml')
    def post(self):
        query = MedicalConsultationModel.query

        hospital = aliased(HospitalModel)
        query = query.outerjoin(hospital, and_(MedicalConsultationModel.hospital_id == hospital.id))

        doctor = aliased(DoctorModel)
        query = query.outerjoin(doctor, and_(MedicalConsultationModel.responsible_doctor_id == doctor.id))

        #Joins para origins
        query = query \
            .outerjoin(DispatchMedicationsModel, MedicalConsultationModel.patient_id == DispatchMedicationsModel.patient_id) \
            .outerjoin(PatientModel, MedicalConsultationModel.patient_id == PatientModel.id) \
            .group_by(MedicalConsultationModel.id)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'patient_id', lambda x: MedicalConsultationModel.patient_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'hospital',
                                                lambda x: func.lower(hospital.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_consultation',
                                                lambda x: func.to_char(MedicalConsultationModel.date_consultation,
                                                                       'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'responsible_doctor',
                                                lambda x: or_(
                                                    func.lower(doctor.document_number).contains(func.lower(x)),
                                                    func.lower(doctor.firstname).contains(func.lower(x)),
                                                    func.lower(doctor.lastname).contains(func.lower(x))
                                                )) # busca por numero de documento, nombres o apellido
            or_filter_list = restrict_collector(or_filter_list, filters, 'observation',
                                                lambda x: func.lower(MedicalConsultationModel.observation).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'origin',
                                                lambda x: or_(
                                                    func.lower(MedicalConsultationModel.origin).contains(func.lower(x)),
                                                    func.lower(DispatchMedicationsModel.origin).contains(
                                                        func.lower(x)),
                                                    func.lower(PatientModel.origin).contains(
                                                        func.lower(x))
                                                ))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        # default order
        query = query.order_by(MedicalConsultationModel.id.desc())

        return paginated_results(query)
