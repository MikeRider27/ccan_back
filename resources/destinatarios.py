import logging

from flasgger import swag_from
from flask import request, jsonify
from flask_babel import _

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy.orm import aliased, selectinload

from models.destinatarios import DestinatariosModel
from models.hospital import HospitalModel
from models.message import MessageModel
from models.notificaciones import NotificacionesModel
from models.parameter import ParameterModel
from models.user import UserModel
from security import check
from utils import paginated_results, restrict_collector, sorting_relationship_type
from sqlalchemy import and_, or_, func


class Destinatarios(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('message_id', type=int)
    parser.add_argument('destinatarios_id', type=int, action='append')
    parser.add_argument('estado_id', type=int)
    parser.add_argument('isborrado', type=bool)

    @jwt_required()
    @check('inbox_get')
    @swag_from('../swagger/inbox/get_inbox.yaml')
    def get(self, id):
        destinatarios = DestinatariosModel.query.filter_by(message_id=id).all()
        if destinatarios:
            return [destinatario.json(jsondepth=1) for destinatario in destinatarios], 200
        return {'message': _("INBOX_NOT_FOUND")}, 404

    @jwt_required()
    @check('inbox_update')
    @swag_from('../swagger/inbox/put_inbox.yaml')
    def put(self, id):
        destinatarios = DestinatariosModel.find_by_id(id)
        if destinatarios:
            newdata = Destinatarios.parser.parse_args()
            DestinatariosModel.from_reqparse(destinatarios, newdata)
            destinatarios.save_to_db()
            return destinatarios.json()
        return {'message': _("INBOX_NOT_FOUND")}, 404

    @jwt_required()
    @check('inbox_delete')
    @swag_from('../swagger/inbox/delete_inbox.yaml')
    def delete(self, id):
        destinatarios = DestinatariosModel.find_by_id(id)
        if destinatarios:
            destinatarios.delete_from_db()

        return {'message': _("INBOX_DELETED")}


class DestinatariosList(Resource):

    @jwt_required()
    @check('inbox_list')
    @swag_from('../swagger/inbox/list_inbox.yaml')
    def get(self):
        query = DestinatariosModel.query
        return query

    @jwt_required()
    @check('inbox_insert')
    @swag_from('../swagger/inbox/post_inbox.yaml')
    def post(self):
        data = Destinatarios.parser.parse_args()

        id = data.get('id')

        if id is not None and DestinatariosModel.find_by_id(id):
            return {'message': _("INBOX_DUPLICATED").format(id)}, 400

        message_id = data.get('message_id')
        destinatarios_ids = data.get('destinatarios_id')  #Array de destinatarios
        estado_id = data.get('estado_id')

        if not destinatarios_ids:
            return {'message': 'Debe proporcionar al menos un destinatario'}, 400

        for destinatario_id in destinatarios_ids:
            # Crear un mensaje para cada destinatario
            message = DestinatariosModel(
                message_id=message_id,
                destinatarios_id=destinatario_id,
                estado_id=estado_id
            )
            try:
                message.save_to_db()

                # Crear una notificación para cada destinatario
                notificacion = NotificacionesModel(
                    user_id=destinatario_id,
                    message_id=message_id
                )
                notificacion.save_to_db()
            except Exception as e:
                logging.error('An error occurred while creating message.', exc_info=e)
                return {"message": 'Error al crear el mensaje'}, 500

        return message.json(), 201


class DestinatariosSearch(Resource):
    @jwt_required()
    @check('inbox_search')
    @swag_from('../swagger/inbox/search_inbox.yaml')
    def post(self):

        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(user=current_user).first()
        destinatarios_id = user.id if user else None

        query = DestinatariosModel.query

        receptor = aliased(UserModel)
        query = query.join(receptor, and_(DestinatariosModel.destinatarios_id == receptor.id))

        mensaje = aliased(MessageModel)
        query = query.join(mensaje, and_(DestinatariosModel.message_id == mensaje.id))

        estado = aliased(ParameterModel)
        query = query.join(estado, and_(DestinatariosModel.estado_id == estado.id))

        emisor = aliased(UserModel)
        query = query.join(emisor, and_(mensaje.emisor_id == emisor.id))

        hospital = aliased(HospitalModel)
        query = query.outerjoin(hospital, and_(mensaje.id_hospital == hospital.id))

        query = query.filter(DestinatariosModel.isborrado == False)  #Muestra los mensajes no borrados

        and_filter_list = []
        or_filter_list = []

        if request.json:
            filters = request.json
            or_filter_list = restrict_collector(or_filter_list, filters, 'message_date',
                                                lambda x: func.to_char(mensaje.fecha_mensaje,
                                                                       'DD/MM/YYYY, HH24:MI').contains(x))
            or_filter_list = restrict_collector(or_filter_list, filters, 'emisor',
                                                lambda x: func.lower(emisor.user).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'estado',
                                                lambda x: func.lower(estado.value).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'asunto',
                                                lambda x: func.lower(mensaje.asunto).contains(func.lower(x)))
            or_filter_list = restrict_collector(or_filter_list, filters, 'hospital',
                                                lambda x: func.lower(hospital.description).contains(func.lower(x)))

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        if destinatarios_id:
            query = query.filter(DestinatariosModel.destinatarios_id == destinatarios_id)

        sort = True
        sort_by = request.args.get('sortBy', None, str)
        if sort_by:
            if sort_by == 'message_date':
                query = sorting_relationship_type(request, query, mensaje.fecha_mensaje)
                sort = False
            if sort_by == 'emisor':
                query = sorting_relationship_type(request, query, emisor.user)
                sort = False
            if sort_by == 'hospital':
                query = sorting_relationship_type(request, query, hospital.description)
                sort = False
            if sort_by == 'estado':
                query = sorting_relationship_type(request, query, estado.value)
                sort = False
            if sort_by == 'asunto':
                query = sorting_relationship_type(request, query, mensaje.asunto)
                sort = False

        return paginated_results(query, sort)
