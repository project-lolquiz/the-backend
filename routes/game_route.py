from flasgger import swag_from
from flask import jsonify, Blueprint

from services.game_service import *

game_config_rest = Blueprint('game_config_rest', __name__)


@game_config_rest.route('/games/configs/types')
@swag_from('./docs/game/game_types.yml')
def game_types():
    return jsonify(get_all_types()), 200


@game_config_rest.route('/games/configs/modes')
@swag_from('./docs/game/game_modes.yml')
def game_modes():
    return jsonify(get_all_modes()), 200
