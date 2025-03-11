import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_babel import _

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy.orm import aliased

from models.destinatarios import DestinatariosModel
from models.message import MessageModel
from models.parameter import ParameterModel
from models.user import UserModel
from security import check
from utils import paginated_results, restrict_collector, sorting_relationship_type
from sqlalchemy import and_, or_, func

class Message(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('asunto', type=str)
    parser.add_argument('mensaje', type=str)
    parser.add_argument('fecha_mensaje', type=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
    parser.add_argument('emisor_id', type=int)
    parser.add_argument('isborrado', type=bool)
    parser.add_argument('id_hospital', type=int)
    parser.add_argument('patient_id', type=int)
    @jwt_required()
    @check('message_get')
    @swag_from('../swagger/message/get_message.yaml')
    def get(self, id):
        message = MessageModel.find_by_id(id)
        if message:
            return message.json()
        return {'message': _("MESSAGE_NOT_FOUND")}, 404

    @jwt_required()
    @check('message_update')
    @swag_from('../swagger/message/put_message.yaml')
    def put(self, id):
        message = MessageModel.find_by_id(id)
        if message:
            message.isborrado = True
            message.save_to_db()
            return message.json()
        return {'message': _("MESSAGE_NOT_FOUND")}, 404

    @jwt_required()
    @check('message_delete')
    @swag_from('../swagger/message/delete_message.yaml')
    def delete(self, id):
        message = MessageModel.find_by_id(id)
        if message:
            message.delete_from_db()

        return {'message': _("MESSAGE_DELETED")}


class MessageList(Resource):

    @jwt_required()
    @check('message_list')
    @swag_from('../swagger/message/list_message.yaml')
    def get(self):
        query = MessageModel.query
        return query

    @jwt_required()
    @check('message_insert')
    @swag_from('../swagger/message/post_message.yaml')
    def post(self):

        current_user = get_jwt_identity()
        user_id = UserModel.query.filter_by(user=current_user).first()
        if user_id:
            emisor_id = user_id.id
        else:
            emisor_id = None

        data = Message.parser.parse_args()
        data['emisor_id'] = emisor_id  # Guardo el id de la persona logueada

        id = data.get('id')

        if id is not None and MessageModel.find_by_id(id):
            return {'message': _("MESSAGE_DUPLICATED").format(id)}, 400

        message = MessageModel(**data)
        try:
            message.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating message.', exc_info=e)
            return {"message": _("MESSAGE_CREATE_ERROR")}, 500

        return message.json(), 201


class MessageSearch(Resource):
    @jwt_required()
    @check('message_search')
    @swag_from('../swagger/message/search_message.yaml')
    def post(self):

        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(user=current_user).first()
        emisor_id = user.id if user else None

        query = MessageModel.query

        emisor = aliased(UserModel)
        query = query.join(emisor, and_(MessageModel.emisor_id == emisor.id, ))

        # Join con Destinatarios para los filtros y el ordenamiento
        destinatarios = aliased(DestinatariosModel, name='destinatarios')
        user_destinatario = aliased(UserModel, name='user_destinatario')  # Alias para los destinatarios
        estado = aliased(ParameterModel)
        query = query.outerjoin(destinatarios, and_(MessageModel.id == destinatarios.message_id))
        query = query.outerjoin(user_destinatario, and_(user_destinatario.id == destinatarios.destinatarios_id))
        query = query.outerjoin(estado, and_(estado.id == destinatarios.estado_id))

        query = query.filter(MessageModel.isborrado == False)

        and_filter_list = []
        or_filter_list = []

        if request.json:
            filters = request.json

            or_filter_list = restrict_collector(or_filter_list, filters, 'message_date',
                                                lambda x: func.to_char(MessageModel.fecha_mensaje,
                                                                       'DD/MM/YYYY, HH24:MI').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'asunto',
                                                lambda x: func.lower(MessageModel.asunto).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'destinatarios_user',
                                                lambda x: func.lower(user_destinatario.user).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'estado',
                                                lambda x: func.lower(estado.value).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        if emisor_id:
            query = query.filter(MessageModel.emisor_id == emisor_id)

        query = query.distinct()
        sort = True
        sort_by = request.args.get('sortBy', None, str)
        if sort_by:
            if sort_by == 'message_date':
                query = sorting_relationship_type(request, query, MessageModel.fecha_mensaje)
                sort = False
            if sort_by == 'destinatarios_user':
                query = sorting_relationship_type(request, query, user_destinatario.user)
                sort = False
            if sort_by == 'asunto':
                query = sorting_relationship_type(request, query, MessageModel.asunto)
                sort = False
            if sort_by == 'estado':
                query = sorting_relationship_type(request, query, estado.value)
                sort = False

        return paginated_results(query, sort)
