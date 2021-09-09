import json
import os
import pytest

os.environ['ENV'] = 'qa'

from components.exception_component import RoomNotFound
from services.games.game_service import start_new_game
from services.games.questions.answers.answer_service import set_answer
from services.games.questions.question_service import get_game_round
from services.redis_service import get_by_key, set_content
from tests.services.games.test_game import create_game_room, request_start_game_body, DEFAULT_USERS_UID
from tests.services.rooms.test_room import DEFAULT_SELECTED_USER_UID


def test_set_answer_with_only_one_right_answer():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)
    set_game_round(room_id)
    body = create_answer_body()

    answer_response = set_answer(room_id, body)
    assert_answer_response(answer_response)
    users_right_answers = [user for user in answer_response['users'] if user['correct_answer']]
    assert len(users_right_answers) == 1


def test_set_answer_with_all_users_right_answer():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)
    set_game_round(room_id)
    body = create_answer_body()
    body['users'][1]['chosen_answer'] = body['users'][0]['chosen_answer']

    answer_response = set_answer(room_id, body)
    assert_answer_response(answer_response)
    users_right_answers = [user for user in answer_response['users'] if user['correct_answer']]
    assert len(users_right_answers) == 2


def test_set_answer_with_all_users_wrong_answer():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)
    set_game_round(room_id)
    body = create_answer_body()
    body['users'][0]['chosen_answer'] = DEFAULT_SELECTED_USER_UID
    body['users'][1]['chosen_answer'] = DEFAULT_SELECTED_USER_UID

    answer_response = set_answer(room_id, body)
    assert_answer_response(answer_response)
    users_right_answers = [user for user in answer_response['users'] if user['correct_answer']]
    assert len(users_right_answers) == 0


def test_failure_set_answer_with_room_not_found():
    room_id = '1AB3'

    with pytest.raises(RoomNotFound, match='Room ID {} not found'.format(room_id)):
        set_answer(room_id, None)


def test_set_answer_with_only_one_right_answer_for_ended_game():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)
    set_ended_game(room_id)
    body = create_answer_body()

    answer_response = set_answer(room_id, body)
    assert_answer_response(answer_response)
    assert_ended_game(answer_response)
    users_right_answers = [user for user in answer_response['users'] if user['correct_answer']]
    assert len(users_right_answers) == 1


def test_set_answer_with_all_users_right_answer_for_ended_and_draw_game():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)
    set_ended_game(room_id)
    body = create_answer_body()
    body['users'][1]['chosen_answer'] = body['users'][0]['chosen_answer']

    answer_response = set_answer(room_id, body)
    assert_answer_response(answer_response)
    assert_ended_game(answer_response)
    assert_draw_game(answer_response)
    users_right_answers = [user for user in answer_response['users'] if user['correct_answer']]
    assert len(users_right_answers) == 2


def test_set_answers_with_only_one_right_answer_and_incrementing_scores():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)
    set_game_round(room_id)

    for index in range(0, len(DEFAULT_USERS_UID)):
        body = create_answer_body()

        answer_response = set_answer(room_id, body)
        assert_answer_response(answer_response)
        users_right_answers = [user for user in answer_response['users'] if user['correct_answer']]
        assert len(users_right_answers) == 1


def set_game_round(room_id):
    current_room = json.loads(get_by_key(room_id))
    get_game_round(room_id, current_room)


def set_ended_game(room_id):
    current_room = json.loads(get_by_key(room_id))
    current_round = {'current': current_room['total_rounds'],
                     'total': current_room['total_rounds']}
    current_room['game']['round'] = current_round
    set_content(room_id, current_room)


def assert_answer_response(answer_response):
    assert answer_response is not None
    assert 'users' in answer_response
    assert len(answer_response['users']) > 0
    assert 'draw' in answer_response
    assert 'end_game' in answer_response


def assert_ended_game(answer_response):
    assert answer_response['end_game']


def assert_draw_game(answer_response):
    assert answer_response['draw']


def create_answer_body():
    users = []
    for user in DEFAULT_USERS_UID:
        users.append({'uid': user,
                      'chosen_answer': user})
    users.append({'uid': DEFAULT_SELECTED_USER_UID,
                  'chosen_answer': DEFAULT_USERS_UID[0]})

    return {'users': users,
            'selected_user_id': DEFAULT_SELECTED_USER_UID}