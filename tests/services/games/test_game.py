import os
import pytest

os.environ['ENV'] = 'qa'

from services.games.game_service import *
from services.rooms.room_service import create_room

from tests.services.rooms.test_room import request_room_body


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


def create_game_room():
    return create_room(request_room_body())


def request_start_game_body():
    return {'users': [{'uid': '8852c5af-a6e5-4fad-9022-3d10ed111a30', 'nickname': 'bet64'},
                      {'uid': 'bbac28f0-5922-4935-9ca7-a313db5ba75a', 'nickname': 'avaii'}]}