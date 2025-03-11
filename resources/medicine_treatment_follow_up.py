import logging

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from flask_babel import _

from models.medicine_treatment_follow_up import MedicineTreatmentFollowUpModel
from utils import restrict, paginated_results
from security import check



class MedicineTreatmentFollowUp(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('medicine_id', type=int)
    parser.add_argument('treatment_follow_up_id', type=int)
    parser.add_argument('quantity', type=float)
    parser.add_argument('observation', type=str)
    parser.add_argument('dose', type=float)
    parser.add_argument('presentation', type=str)
    parser.add_argument('concentration', type=str)
    parser.add_argument('deposit_stock_id', type=int)

    @jwt_required()
    @check('medicine_treatment_follow_up_get')
    @swag_from('../swagger/medicine_treatment_follow_up/get_medicine_treatment_follow_up.yaml')
    def get(self, id):
        medicine_treatment_follow_up = MedicineTreatmentFollowUpModel.find_by_id(id)
        if medicine_treatment_follow_up:
            return medicine_treatment_follow_up.json()
        return {'message': _("MEDICINE_TREATMENT_FOLLOW_UP_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_treatment_follow_up_update')
    @swag_from('../swagger/medicine_treatment_follow_up/put_medicine_treatment_follow_up.yaml')
    def put(self, id):
        medicine_treatment_follow_up = MedicineTreatmentFollowUpModel.find_by_id(id)
        if medicine_treatment_follow_up:
            newdata = MedicineTreatmentFollowUp.parser.parse_args()
            MedicineTreatmentFollowUpModel.from_reqparse(medicine_treatment_follow_up, newdata)
            medicine_treatment_follow_up.save_to_db()
            return medicine_treatment_follow_up.json()
        return {'message': _("MEDICINE_TREATMENT_FOLLOW_UP_NOT_FOUND")}, 404

    @jwt_required()
    @check('medicine_treatment_follow_up_delete')
    @swag_from('../swagger/medicine_treatment_follow_up/delete_medicine_treatment_follow_up.yaml')
    def delete(self, id):
        medicine_treatment_follow_up = MedicineTreatmentFollowUpModel.find_by_id(id)
        if medicine_treatment_follow_up:
            medicine_treatment_follow_up.delete_from_db()

        return {'message': _("MEDICINE_TREATMENT_FOLLOW_UP_DELETED")}


class MedicineTreatmentFollowUpList(Resource):

    @jwt_required()
    @check('medicine_treatment_follow_up_list')
    @swag_from('../swagger/medicine_treatment_follow_up/list_medicine_treatment_follow_up.yaml')
    def get(self):
        query = MedicineTreatmentFollowUpModel.query
        return paginated_results(query)

    @jwt_required()
    @check('medicine_treatment_follow_up_insert')
    @swag_from('../swagger/medicine_treatment_follow_up/post_medicine_treatment_follow_up.yaml')
    def post(self):
        data = MedicineTreatmentFollowUp.parser.parse_args()

        id = data.get('id')

        if id is not None and MedicineTreatmentFollowUpModel.find_by_id(id):
            return {'message': _("MEDICINE_TREATMENT_FOLLOW_UP_DUPLICATED").format(id)}, 400

        medicine_treatment_follow_up = MedicineTreatmentFollowUpModel(**data)
        try:
            medicine_treatment_follow_up.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating Medicine treatment follow up.', exc_info=e)
            return {"message": _("MEDICINE_TREATMENT_FOLLOW_UP_CREATE_ERROR")}, 500

        return medicine_treatment_follow_up.json(), 201


class MedicineTreatmentFollowUpSearch(Resource):

    @jwt_required()
    @check('medicine_treatment_follow_up_search')
    @swag_from('../swagger/medicine_treatment_follow_up/search_medicine_treatment_follow_up.yaml')
    def post(self):
        query = MedicineTreatmentFollowUpModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: MedicineTreatmentFollowUpModel.id == x)
            query = restrict(query, filters, 'medicine_id', lambda x: MedicineTreatmentFollowUpModel.medicine_id == x)
            query = restrict(query, filters, 'treatment_follow_up_id', lambda x: MedicineTreatmentFollowUpModel.treatment_follow_up_id == x)
            query = restrict(query, filters, 'observation', lambda x: MedicineTreatmentFollowUpModel.observation.contains(x))
            query = restrict(query, filters, 'presentation',
                             lambda x: MedicineTreatmentFollowUpModel.presentation.contains(x))
            query = restrict(query, filters, 'concentration',
                             lambda x: MedicineTreatmentFollowUpModel.concentration.contains(x))

        # default order
        query = query.order_by(MedicineTreatmentFollowUpModel.id.desc())
        return paginated_results(query)
