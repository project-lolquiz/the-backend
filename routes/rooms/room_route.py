from flasgger import swag_from
from flask import jsonify, Blueprint, request, current_app
from flask_expects_json import expects_json

from services.rooms.room_service import *
from ..default_route import json_error_message
from ..schemas.room_schema import *

room_rest = Blueprint('room_rest', __name__)


@room_rest.route('/games/rooms', methods=['post'])
@expects_json(post_schema)
@swag_from('../docs/room/room_create.yml')
def create_game_room():
    response = {'room_id': create_room(request.get_json())}
    return jsonify(response), 201


@room_rest.route('/games/rooms/<string:room_id>')
@swag_from('../docs/room/room_get.yml')
def check_exists_room(room_id):
    response = {'exists': exists_room_by_id(room_id)}
    return jsonify(response), 200


@room_rest.route('/games/rooms/<string:room_id>/host_user', methods=['put'])
@expects_json(host_user_schema)
@swag_from('../docs/room/host_user/host_user.yml')
def set_host_user(room_id):
    try:
        change_host_user(room_id, request.get_json())
    except RoomNotFound as rnf:
        return json_error_message(rnf.message), 404
    except Exception as e:
        current_app.logger.error(e)
        return json_error_message(str(e)), 500
    return {}, 204
