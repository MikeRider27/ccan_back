import logging

from flasgger import swag_from
from flask import request, jsonify
from flask_babel import _
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError

from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from models.notificaciones import NotificacionesModel
from models.user import UserModel

from security import check
from utils import restrict, paginated_results, restrict_collector


class Notificaciones(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('user_id', type=int)
    parser.add_argument('message_id', type=int)
    parser.add_argument('leida', type=bool)

    @jwt_required()
    @check('notificaciones_get')
    @swag_from('../swagger/notificaciones/get_notificaciones.yaml')
    def get(self, id):
        notifications = NotificacionesModel.find_by_id(id)
        if notifications:
            return notifications.json()
        return {'message': _("NOTIFICATIONS_NOT_FOUND")}, 404

    @jwt_required()
    @check('notificaciones_update')
    @swag_from('../swagger/notificaciones/put_notificaciones.yaml')
    def put(self, id):
        notification = NotificacionesModel.find_by_id(id)
        if notification:
            newdata = Notificaciones.parser.parse_args()
            NotificacionesModel.from_reqparse(notification, newdata)
            notification.save_to_db()
            return notification.json()
        return {'message': _("NOTIFICATION_NOT_FOUND")}, 404


class NotificacionesList(Resource):

    @jwt_required()
    @check('notificaciones_list')
    @swag_from('../swagger/notificaciones/list_notificaciones.yaml')
    def get(self):
        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(user=current_user).first()

        notificaciones = NotificacionesModel.query.filter_by(user_id=user.id, leida=False).all()
        notificaciones_list = [n.json() for n in notificaciones]

        return jsonify(notificaciones_list)

    @jwt_required()
    @check('notificaciones_insert')
    @swag_from('../swagger/notificaciones/post_notificaciones.yaml')
    def post(self):
        data = request.json
        user_id = data.get('user_id')
        message_id = data.get('message_id')

        nueva_notificacion = NotificacionesModel(user_id=user_id, message_id=message_id)
        try:
            nueva_notificacion.save_to_db()
        except Exception as e:
            logging.error('An error occurred while creating notification.', exc_info=e)
            return {"message": _("NOTIFICATION_CREATE_ERROR")}, 500

        return {"message": "Notificación creada exitosamente"}, 201


class NotificacionesSearch(Resource):
    @jwt_required()
    @check('notificaciones_search')
    @swag_from('../swagger/notificaciones/search_notificaciones.yaml')
    def post(self):
        query = NotificacionesModel.query
        and_filter_list = []
        or_filter_list = []
        if request.json:
            filters = request.json
            and_filter_list = restrict_collector(and_filter_list, filters, 'destinatario', lambda x: NotificacionesModel.user_id == x)
            and_filter_list = restrict_collector(and_filter_list, filters, 'mensaje', lambda x: NotificacionesModel.message_id == x)

        # Apply filters
        query = query.filter(and_(*and_filter_list, or_(*or_filter_list)))

        return paginated_results(query)
