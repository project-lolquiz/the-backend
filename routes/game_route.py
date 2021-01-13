from flask import jsonify, Blueprint, request

from services.game_service import *

game_rest = Blueprint('game_rest', __name__)


@game_rest.route('/games/types')
def game_types():
    return jsonify(get_all_types()), 200


@game_rest.route('/games/modes')
def game_modes():
    return jsonify(get_all_modes()), 200
