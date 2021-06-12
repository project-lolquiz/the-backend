from flasgger import swag_from
from flask import jsonify, Blueprint, request
from flask_expects_json import expects_json

from services.rooms.room_service import *
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