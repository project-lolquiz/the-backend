from flasgger import swag_from
from flask import Blueprint, request
from flask_expects_json import expects_json

from routes.default_route import json_error_message
from services.games.game_service import *
from ..schemas.game_schema import *

game_rest = Blueprint('game_rest', __name__)


@game_rest.route('/games/<string:room_id>/start', methods=['post'])
@expects_json(start_game_schema)
@swag_from('../docs/game/start_game.yml')
def start_game(room_id):
    try:
        start_new_game(request.get_json(), room_id)
    except RoomNotFound as rnf:
        return json_error_message(rnf.message), 404
    return '', 201
