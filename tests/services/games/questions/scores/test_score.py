import json
import os
import pytest

os.environ['ENV'] = 'qa'

from components.exception_component import RoomNotFound
from services.games.game_service import start_new_game
from services.games.questions.answers.answer_service import set_answer
from services.games.scores.score_service import get_result_score, is_draw_game_from_current_room, is_draw_game
from services.games.questions.question_service import get_game_round
from services.redis_service import get_by_key
from tests.services.games.questions.answers.test_answer import create_answer_body
from tests.services.games.test_game import create_game_room, request_start_game_body
from tests.services.rooms.test_room import DEFAULT_SELECTED_USER_UID


def test_get_result_score_with_a_winner():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    current_room = json.loads(get_by_key(room_id))
    get_game_round(room_id, current_room)

    body = create_answer_body()
    body['users'][0]['chosen_answer'] = DEFAULT_SELECTED_USER_UID
    set_answer(room_id, body)

    result_score = get_result_score(room_id)
    assert_result_score(result_score)
    assert result_score['winner'] is not None
    assert result_score['winner']['uid'] != DEFAULT_SELECTED_USER_UID


def test_get_result_score_with_selected_user_as_winner():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    current_room = json.loads(get_by_key(room_id))
    get_game_round(room_id, current_room)

    body = create_answer_body()
    set_answer(room_id, body)

    result_score = get_result_score(room_id)
    assert_result_score(result_score)
    assert result_score['winner'] is not None
    assert result_score['winner']['uid'] == DEFAULT_SELECTED_USER_UID


# Draw game
def test_get_result_score_without_a_winner():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    current_room = json.loads(get_by_key(room_id))
    get_game_round(room_id, current_room)

    body = create_answer_body()
    body['users'][0]['chosen_answer'] = DEFAULT_SELECTED_USER_UID
    body['users'][1]['chosen_answer'] = DEFAULT_SELECTED_USER_UID
    set_answer(room_id, body)

    result_score = get_result_score(room_id)
    assert_result_score(result_score)
    assert result_score['winner'] is None


def test_failure_get_result_score_with_room_not_found():
    room_id = '291Y'

    with pytest.raises(RoomNotFound, match='Room ID {} not found'.format(room_id)):
        get_result_score(room_id)


def test_is_draw_game_from_current_room_without_score_by_user_node():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)
    current_room = json.loads(get_by_key(room_id))
    assert not is_draw_game_from_current_room(current_room)


def test_is_draw_game_with_current_score_none():
    assert not is_draw_game(None)


def test_is_draw_game_with_current_score_empty():
    assert not is_draw_game([])


def assert_result_score(result_score):
    assert result_score is not None
    assert 'users' in result_score
    assert 'winner' in result_score

    for user in result_score['users']:
        assert 'uid' in user
        assert 'nickname' in user
        assert 'total_score' in user
