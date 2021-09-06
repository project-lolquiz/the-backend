import os
import pytest

os.environ['ENV'] = 'qa'

from services.games.game_service import *
from services.rooms.room_service import create_room

from tests.services.rooms.test_room import request_room_body, DEFAULT_TOTAL_ROUNDS


def test_success_start_new_game():
    room_id = create_game_room()
    body = request_start_game_body()

    game_room = start_new_game(body, room_id)

    assert game_room
    assert 'game_type' in game_room
    assert 'game_mode' in game_room
    assert 'host_user' in game_room
    assert 'total_rounds' in game_room
    assert 'room_id' in game_room
    assert 'game' in game_room


def test_failure_start_new_game_with_room_not_found():
    room_id = 'CDEF'

    with pytest.raises(RoomNotFound, match='Room ID {} not found'.format(room_id)):
        start_new_game(request_start_game_body(), room_id)


def test_get_game_question():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    game_question = get_game_question(room_id)
    assert_game_question(game_question)


def test_get_another_game_question():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    game_question_01 = get_game_question(room_id)
    assert_game_question(game_question_01)

    game_question_02 = get_game_question(room_id)
    assert_game_question(game_question_02)

    assert game_question_01['selected_user_id'] != game_question_02['selected_user_id']
    assert game_question_01['title'] != game_question_02['title']
    assert game_question_01['round']['current'] < game_question_02['round']['current']


def test_get_different_game_question_accordingly_to_total_rounds():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    selected_titles = []

    for _ in range(0, DEFAULT_TOTAL_ROUNDS):
        game_question = get_game_question(room_id)
        assert_game_question(game_question)

        current_title = game_question['title']
        assert current_title not in selected_titles

        selected_titles.append(current_title)


def assert_game_question(game_question):
    assert game_question is not None
    assert 'selected_user_id' in game_question
    assert 'title' in game_question
    assert 'options' in game_question
    assert len(game_question['options']) > 0
    assert 'round' in game_question
    assert 'current' in game_question['round']
    assert 'total' in game_question['round']
    assert 'draw' in game_question


def test_failure_game_question_with_room_not_found():
    room_id = '14UI'

    with pytest.raises(RoomNotFound, match='Room ID {} not found'.format(room_id)):
        get_game_question(room_id)


def create_game_room():
    return create_room(request_room_body())


def request_start_game_body():
    return {'users': [{'uid': '8852c5af-a6e5-4fad-9022-3d10ed111a30', 'nickname': 'bet64'},
                      {'uid': 'bbac28f0-5922-4935-9ca7-a313db5ba75a', 'nickname': 'avaii'}]}