import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.medical_committee import MedicalCommitteeModel
from security import check
from utils import restrict, paginated_results


class MedicalCommittee(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('committee_id', type=int)
    parser.add_argument('doctor_id', type=int)

    @jwt_required()
    @check('medical_committee_get')
    @swag_from('../swagger/medical_committee/get_medical_committee.yaml')
    def get(self, id):
        medical_committee = MedicalCommitteeModel.find_by_id(id)
        if medical_committee:
            return medical_committee.json()
        return {'message': _("MEDICAL_COMMITTEE_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_committee_update')
    @swag_from('../swagger/medical_committee/put_medical_committee.yaml')
    def put(self, id):
        medical_committee = MedicalCommitteeModel.find_by_id(id)
        if medical_committee:
            newdata = MedicalCommittee.parser.parse_args()
            MedicalCommitteeModel.from_reqparse(medical_committee, newdata)
            medical_committee.save_to_db()
            return medical_committee.json()
        return {'message': _("MEDICAL_COMMITTEE_NOT_FOUND")}, 404

    @jwt_required()
    @check('medical_committee_delete')
    @swag_from('../swagger/medical_committee/delete_medical_committee.yaml')
    def delete(self, id):
        medical_committee = MedicalCommitteeModel.find_by_id(id)
        if medical_committee:
            medical_committee.delete_from_db()

        return {'message': _("MEDICAL_COMMITTEE_DELETED")}


class MedicalCommitteeList(Resource):

    @jwt_required()
    @check('medical_committee_list')
    @swag_from('../swagger/medical_committee/list_medical_committee.yaml')
    def get(self):
        query = MedicalCommitteeModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medical_committee_insert')
    @swag_from('../swagger/medical_committee/post_medical_committee.yaml')
    def post(self):
        data = MedicalCommittee.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicalCommitteeModel.find_by_id(id):
            return {'message': _("MEDICAL_COMMITTEE_DUPLICATED").format(id)}, 400

        medical_committee = MedicalCommitteeModel(**data)
        try:
            medical_committee.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating medical committee.', exc_info=e)
            return {"message": _("MANUFACTURER_CREATE_ERROR")}, 500

        return medical_committee.json(), 201


class MedicalCommitteeSearch(Resource):

    @jwt_required()
    @check('medical_committee_search')
    @swag_from('../swagger/medical_committee/search_medical_committee.yaml')
    def post(self):
        query = MedicalCommitteeModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MedicalCommitteeModel.id == x)
            query = restrict(query, filters, 'committee_id', lambda x: MedicalCommitteeModel.committee_id == x)
            query = restrict(query, filters, 'doctor_id', lambda x: MedicalCommitteeModel.doctor_id == x)

        # default order
        query = query.order_by(MedicalCommitteeModel.id.desc())

        return paginated_results(query)
