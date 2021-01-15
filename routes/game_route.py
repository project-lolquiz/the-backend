from flasgger import swag_from
from flask import jsonify, Blueprint

from services.game_service import *

game_rest = Blueprint('game_rest', __name__)


@game_rest.route('/games/types')
@swag_from('./docs/game/game_types.yml')
def game_types():
    return jsonify(get_all_types()), 200


@game_rest.route('/games/modes')
@swag_from('./docs/game/game_modes.yml')
def game_modes():
    return jsonify(get_all_modes()), 200
