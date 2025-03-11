import logging
from datetime import datetime

from flasgger import swag_from
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy import and_, func, or_, distinct
from sqlalchemy.orm import aliased, Session
from flask_babel import _

from models.document_type import DocumentTypeModel
from models.evaluation import EvaluationModel
from models.evaluators import EvaluatorsModel
from models.gender import GenderModel
from models.parameter import ParameterModel
from models.patient import PatientModel
from models.patient_hospital import PatientHospitalModel
from models.role import RoleModel
from models.user import UserModel
from models.user_role import UserRoleModel
from resources.patient import patient_update_state
from utils import paginated_results, restrict_collector, sorting_relationship_type
from security import check


class Evaluation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('date_start', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('date_end', type=lambda x: datetime.strptime(x, '%d/%m/%Y').date())
    parser.add_argument('observation', type=str)
    parser.add_argument('evaluator_list', type=list, location='json')
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('user_modify', type=str)
    parser.add_argument('evaluation_state', type=str)

    @jwt_required()
    @check('evaluation_get')
    @swag_from('../swagger/evaluation/get_evaluation.yaml')
    def get(self, id):
        evaluation = EvaluationModel.find_by_id(id)
        if evaluation:
            return evaluation.json()
        return {'message': _("EVALUATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('evaluation_update')
    @swag_from('../swagger/evaluation/put_evaluation.yaml')
    def put(self, id):
        evaluation: EvaluationModel = EvaluationModel.find_by_id(id)
        if evaluation:
            newdata = Evaluation.parser.parse_args()
            evaluator_data_list = newdata['evaluator_list']
            EvaluationModel.from_reqparse(evaluation, newdata)

            # evaluator_list update
            evaluator_list = []
            for evaluator in evaluator_data_list:
                if evaluator.get('id', None):
                    evaluator_model = EvaluatorsModel.find_by_id(evaluator['id'])
                    EvaluatorsModel.from_reqparse(evaluator_model, evaluator)
                else:
                    evaluator_model = EvaluatorsModel(**evaluator)
                evaluator_list.append(evaluator_model)

            evaluation.evaluator_list = evaluator_list

            evaluation.user_modify = get_jwt_identity()
            evaluation.date_modify = datetime.now()
            evaluation.save_to_db()

            # LLamar evento de cambio de estado de paciente
            patient_update_state(newdata.get('patient_id', None))

            return evaluation.json()
        return {'message': _("EVALUATION_NOT_FOUND")}, 404

    @jwt_required()
    @check('evaluation_delete')
    @swag_from('../swagger/evaluation/delete_evaluation.yaml')
    def delete(self, id):
        evaluation = EvaluationModel.find_by_id(id)
        if evaluation:
            evaluation.delete_from_db()

        return {'message': _("EVALUATION_DELETED")}


class EvaluationList(Resource):
    @jwt_required()
    @check('evaluation_list')
    @swag_from('../swagger/evaluation/list_evaluation.yaml')
    def get(self):
        query = EvaluationModel.query
        return paginated_results(query)

    @jwt_required()
    @check('evaluation_insert')
    @swag_from('../swagger/evaluation/post_evaluation.yaml')
    def post(self):
        data = Evaluation.parser.parse_args()

        id = data.get('id')
        if id is not None and EvaluationModel.find_by_id(id):
            return {'message': _("EVALUATION_DUPLICATED").format(id)}, 400

        patient_id = data.get('patient_id', None)
        if patient_id:
            patient = PatientModel.find_by_id(patient_id)
            if patient:
                if patient.state.code != 'EVAL' and patient.state.code != 'REV':
                    return {'message': _("EVALUATION_STATUS")}, 400

        evaluator_data_list = data['evaluator_list']
        del data['evaluator_list']
        evaluation: EvaluationModel = EvaluationModel(**data)

        for evaluator in evaluator_data_list:
            evaluator_model = EvaluatorsModel(**evaluator)
            evaluation.evaluator_list.append(evaluator_model)

        try:
            evaluation.user_create = get_jwt_identity()
            evaluation.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating evaluation', exc_info=e)
            return {"message": _("EVALUATION_CREATE_ERROR")}, 500

        # LLamar evento de cambio de estado de paciente
        patient_update_state(data.get('patient_id', None))

        return evaluation.json(), 201


class EvaluationSearch(Resource):
    @jwt_required()
    @check('evaluation_search')
    @swag_from('../swagger/evaluation/search_evaluation.yaml')
    def post(self):
        query = EvaluationModel.query

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            # query = restrict(query, filters, 'id', lambda x: EvaluationModel.id == x)
            and_filter_list = restrict_collector(and_filter_list, filters, 'patient_id', lambda x: EvaluationModel.patient_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'observation', lambda x: EvaluationModel.observation.contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_start', lambda x: func.to_char(EvaluationModel.date_start, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'date_end', lambda x: func.to_char(EvaluationModel.date_end, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_create', lambda x: EvaluationModel.user_create.contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'user_modify', lambda x: EvaluationModel.user_modify.contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'evaluation_state', lambda x: EvaluationModel.approved.contains(x))

        # Apply filters
        general_filter = request.args.get('general_filter', None, str) == 'true'
        if general_filter:
            query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
        else:
            filter_list = and_filter_list + or_filter_list
            query = query.filter(and_(*filter_list))

        # default order
        query = query.order_by(EvaluationModel.id.desc())
        return paginated_results(query)


class PatientEvaluationSearch(Resource):
    @jwt_required()
    @check('patient_evaluation_search')
    @swag_from('../swagger/evaluation/search_evaluation.yaml')
    def post(self):
        key = current_app.config['ENCRYPTION_KEY']
        query = PatientModel.query
        hospital_id = request.json.get('hospital_id')

        # Relationship
        state = aliased(ParameterModel)
        query = query.join(state, and_(PatientModel.state_id == state.id,
                                       state.domain == 'PATIENT_STATE'), isouter=True)
        document_type = aliased(DocumentTypeModel)
        query = query.join(document_type, PatientModel.document_type_id == document_type.id, isouter=True)
        gender = aliased(GenderModel)
        query = query.join(gender, PatientModel.gender_id == gender.id, isouter=True)

        # Join condicional por filtro debido a duplicacion por tabla intermedia
        if hospital_id:
            patient_hospital = aliased(PatientHospitalModel)
            query = query.join(patient_hospital, PatientModel.id == patient_hospital.patient_id, isouter=True)

        evaluation = aliased(EvaluationModel)
        query = query.join(evaluation, PatientModel.id == evaluation.patient_id, isouter=True)

        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            or_filter_list = restrict_collector(or_filter_list, filters, 'firstname', lambda x: func.lower(
                func.decrypt_data(PatientModel.firstname, key)).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'lastname', lambda x: func.lower(
                func.decrypt_data(PatientModel.lastname, key)).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'document_number', lambda x: func.lower(
                func.decrypt_data(PatientModel.document_number, key)).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'birthdate',
                                                lambda x: func.to_char(PatientModel.birthdate, 'DD/MM/YYYY').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'registration_date',
                                                lambda x: func.to_char(PatientModel.registration_date,
                                                                       'DD/MM/YYYY').contains(x))

            # Relationship Filter
            # Join condicional por filtro
            if hospital_id:
                and_filter_list = restrict_collector(and_filter_list, filters, 'hospital_id', lambda x: patient_hospital.hospital_id == x)
            or_filter_list = restrict_collector(or_filter_list, filters, 'state',
                                                lambda x: func.lower(state.value).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'document_type',
                                                lambda x: func.lower(document_type.description).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'gender',
                                                lambda x: func.lower(gender.description).contains(func.lower(x)))

            # Se filtra los pacientes en evaluacion aquellos que:
            # 1. No tienen estado sospechoso
            # 2. Tienen estado EVAL o REV
            # 3. Los demas estados si y solo si tienen algun registro en la tabla Evaluación
            session = Session()
            query = query.filter(
                ~state.code.in_(['SOSP']),
                or_(
                    state.code.in_(['EVAL', 'REV']),
                    and_(
                        ~state.code.in_(['SOSP']),
                        PatientModel.id.in_(session.query(distinct(EvaluationModel.patient_id)))
                    )
                )
            ).distinct()

            # Se agregan columnas del order by por usar el distinct
            query = query.add_column(func.decrypt_data(PatientModel.document_number, key))
            query = query.add_column(func.decrypt_data(PatientModel.firstname, key))
            query = query.add_column(func.decrypt_data(PatientModel.lastname, key))

            # Apply filters
            general_filter = request.args.get('general_filter', None, str) == 'true'
            if general_filter:
                query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))
            else:
                filter_list = and_filter_list + or_filter_list
                query = query.filter(and_(*filter_list))

        # Capture Relationship Sorting and configure performance
        sort = True
        sort_by = request.args.get('sortBy', None, str)
        if sort_by:
            if sort_by == 'state':
                query = sorting_relationship_type(request, query, state.value)
                sort = False
            elif sort_by == 'document_type':
                query = sorting_relationship_type(request, query, document_type.description)
                sort = False
            elif sort_by == 'gender':
                query = sorting_relationship_type(request, query, gender.description)
                sort = False

        return paginated_results(query, sort, is_patient=True)


class UsersEvaluator(Resource):
    @jwt_required()
    # @check('evaluation_user_list')
    # @swag_from('../swagger/evaluation/evaluation_luser_list.yaml')
    def post(self):
        query = UserModel.query
        query = query.join(UserRoleModel, and_(UserRoleModel.user_id == UserModel.id))
        query = query.join(RoleModel, and_(RoleModel.id == UserRoleModel.role_id, RoleModel.description == 'EVALUADOR'))

        if request.json:
            filters = request.json
            hospital_id = filters.get('hospital_id', None)
            if hospital_id:
                query = query.filter(UserRoleModel.hospital_id == hospital_id)

        return paginated_results(query)


class EvaluationComplete(Resource):
    @jwt_required()
    # @check('evaluation_complete')
    # @swag_from('../swagger/evaluation/evaluation_luser_list.yaml')

    def put(self, patient_id):
        patient = PatientModel.find_by_id(patient_id)
        if patient:
            eval_state = ParameterModel.query.filter_by(domain='PATIENT_STATE', code='EVAL').first()
            patient.state_id = eval_state.id
            patient.save_to_db(encrypt=False)

            return patient.json(), 200
        return {'message': _("PATIEND_NOT_FOUND")}, 404
