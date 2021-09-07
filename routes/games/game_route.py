from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json

from routes.default_route import json_error_message
from services.games.game_service import *
from services.games.questions.answers.answer_service import set_answer
from services.games.questions.question_service import get_game_question
from services.games.scores.score_service import get_result_score
from ..schemas.game_schema import *
from ..schemas.game_answer_schema import *

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


@game_rest.route('/games/<string:room_id>/questions', methods=['get'])
@swag_from('../docs/game/question/game_question.yml')
def game_question(room_id):
    try:
        return jsonify(get_game_question(room_id)), 200
    except RoomNotFound as rnf:
        return json_error_message(rnf.message), 404


@game_rest.route('/games/<string:room_id>/questions/answers', methods=['post'])
@expects_json(game_answer_schema)
@swag_from('../docs/game/question/answer/game_answer.yml')
def game_answer(room_id):
    try:
        return jsonify(set_answer(room_id, request.get_json())), 201
    except RoomNotFound as rnf:
        return json_error_message(rnf.message), 404


@game_rest.route('/games/<string:room_id>/results/scores', methods=['get'])
@swag_from('../docs/game/question/score/game_score.yml')
def game_result_score(room_id):
    try:
        return jsonify(get_result_score(room_id)), 200
    except RoomNotFound as rnf:
        return json_error_message(rnf.message), 404
