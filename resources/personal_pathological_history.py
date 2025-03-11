import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask_babel import _

from models.patient_family_with_cancer import PatientFamilyWithCancerModel
from models.personal_pathological_history import PersonalPathologicalHistoryModel
from utils import restrict, paginated_results
from security import check


class PersonalPathologicalHistory(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('patient_id', type=int)
    parser.add_argument('family_members_with_cancer', type=str)
    parser.add_argument('cie_10_code_id', type=int)
    parser.add_argument('observation', type=str)
    parser.add_argument('app_funtional_class_nyha_id', type=int)
    parser.add_argument('app_ischemic_heart_disease', type=bool)
    parser.add_argument('app_heart_failure', type=bool)
    parser.add_argument('app_arrhythmia', type=bool)
    parser.add_argument('app_heart_others', type=bool)
    parser.add_argument('app_heart_others_input', type=str)
    parser.add_argument('menopausal_state_id', type=int)
    parser.add_argument('app_menopausal_others', type=str)
    parser.add_argument('fevi_percentage', type=int)
    parser.add_argument('fevi_date', type=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    parser.add_argument('date_create', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_create', type=str)
    parser.add_argument('date_modify', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    parser.add_argument('user_modify', type=str)
    parser.add_argument('family_list', type=list, location='json')
    parser.add_argument('hospital_id', type=int)

    @jwt_required()
    @check('personal_pathological_history_get')
    @swag_from('../swagger/personal_pathological_history/get_personal_pathological_history.yaml')
    def get(self, id):
        personal_pathological_history = PersonalPathologicalHistoryModel.find_by_id(id)
        if personal_pathological_history:
            return personal_pathological_history.json()
        return {'message': _("PERSONAL_PATHOLOGICAL_HISTORY_NOT_FOUND")}, 404

    @jwt_required()
    @check('personal_pathological_history_update')
    @swag_from('../swagger/personal_pathological_history/put_personal_pathological_history.yaml')
    def put(self, id):
        personal_pathological_history = PersonalPathologicalHistoryModel.find_by_id(id)
        if personal_pathological_history:
            newdata = PersonalPathologicalHistory.parser.parse_args()
            family_data_list = newdata['family_list']
            PersonalPathologicalHistoryModel.from_reqparse(personal_pathological_history, newdata)

            # family update
            family_list = []
            for family_data in family_data_list:
                if 'id' in family_data and family_data['id']:
                    family_model = PatientFamilyWithCancerModel.find_by_id(family_data['id'])
                    PatientFamilyWithCancerModel.from_reqparse(family_model, family_data)
                else:
                    family_model = PatientFamilyWithCancerModel(**family_data)
                family_list.append(family_model)

            personal_pathological_history.family_list = family_list

            personal_pathological_history.user_modify = get_jwt_identity()
            personal_pathological_history.date_modify = datetime.now()
            personal_pathological_history.save_to_db()
            return personal_pathological_history.json()
        return {'message': _("PERSONAL_PATHOLOGICAL_HISTORY_NOT_FOUND")}, 404

    @jwt_required()
    @check('personal_pathological_history_delete')
    @swag_from('../swagger/personal_pathological_history/delete_personal_pathological_history.yaml')
    def delete(self, id):
        personal_pathological_history = PersonalPathologicalHistoryModel.find_by_id(id)
        if personal_pathological_history:
            personal_pathological_history.delete_from_db()

        return {'message': _("PERSONAL_PATHOLOGICAL_HISTORY_DELETED")}


class PersonalPathologicalHistoryList(Resource):

    @jwt_required()
    @check('personal_pathological_history_list')
    @swag_from('../swagger/personal_pathological_history/list_personal_pathological_history.yaml')
    def get(self):
        query = PersonalPathologicalHistoryModel.query
        return paginated_results(query)

    @jwt_required()
    @check('personal_pathological_history_insert')
    @swag_from('../swagger/personal_pathological_history/post_personal_pathological_history.yaml')
    def post(self):
        data = PersonalPathologicalHistory.parser.parse_args()

        id = data.get('id')

        if id is not None and PersonalPathologicalHistoryModel.find_by_id(id):
            return {'message': _("PERSONAL_PATHOLOGICAL_HISTORY_DUPLICATED").format(id)}, 400

        family_data_list = data['family_list']
        del data['family_list']
        personal_pathological_history = PersonalPathologicalHistoryModel(**data)

        for family_data in family_data_list:
            family_model = PatientFamilyWithCancerModel(**family_data)
            personal_pathological_history.family_list.append(family_model)

        try:
            personal_pathological_history.user_create = get_jwt_identity()
            personal_pathological_history.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating personal pathological history.', exc_info=e)
            return {"message": _("PERSONAL_PATHOLOGICAL_HISTORY_CREATE_ERROR")}, 500

        return personal_pathological_history.json(), 201


class PersonalPathologicalHistorySearch(Resource):

    @jwt_required()
    @check('personal_pathological_history_search')
    @swag_from('../swagger/personal_pathological_history/search_personal_pathological_history.yaml')
    def post(self):
        query = PersonalPathologicalHistoryModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PersonalPathologicalHistoryModel.id == x)
            query = restrict(query, filters, 'patient_id', lambda x: PersonalPathologicalHistoryModel.patient_id == x)
            query = restrict(query, filters, 'family_members_with_cancer', lambda x: PersonalPathologicalHistoryModel.family_members_with_cancer.contains(x))
            query = restrict(query, filters, 'cie_10_code_id', lambda x: PersonalPathologicalHistoryModel.cie_10_code_id == x)
            query = restrict(query, filters, 'observation', lambda x: PersonalPathologicalHistoryModel.observation.contains(x))
            query = restrict(query, filters, 'app_funtional_class_nyha_id', lambda x: PersonalPathologicalHistoryModel.app_funtional_class_nyha_id == x)
            query = restrict(query, filters, 'app_ischemic_heart_disease', lambda x: x)
            query = restrict(query, filters, 'app_heart_failure', lambda x: x)
            query = restrict(query, filters, 'app_arrhythmia', lambda x: x)
            query = restrict(query, filters, 'app_heart_others', lambda x: x)
            query = restrict(query, filters, 'app_heart_others_input', lambda x: PersonalPathologicalHistoryModel.app_heart_others_input.contains(x))
            query = restrict(query, filters, 'menopausal_state_id', lambda x: PersonalPathologicalHistoryModel.menopausal_state_id == x)
            query = restrict(query, filters, 'app_menopausal_others', lambda x: PersonalPathologicalHistoryModel.app_menopausal_others.contains(x))
            query = restrict(query, filters, 'fevi_percentage', lambda x: PersonalPathologicalHistoryModel.fevi_percentage == x)
            query = restrict(query, filters, 'user_create', lambda x: PersonalPathologicalHistoryModel.user_create.contains(x))
            query = restrict(query, filters, 'user_modify', lambda x: PersonalPathologicalHistoryModel.user_modify.contains(x))
            query = restrict(query, filters, 'hospital_id', lambda x: PersonalPathologicalHistoryModel.hospital_id == x)
        return paginated_results(query)
