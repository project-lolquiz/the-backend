import json
import os
import pytest
import uuid

from components.exception_component import RoomNotFound

os.environ['ENV'] = 'qa'

from services.games.game_service import start_new_game
from services.redis_service import set_content, get_by_key
from services.rooms.room_service import create_room, exists_room_by_id, generate_room_id, change_host_user

DEFAULT_TOTAL_ROUNDS = 10
DEFAULT_SELECTED_USER_UID = '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'


def test_success_create_room():
    room_body = request_room_body()
    room_id = create_room(room_body)
    assert room_id
    assert len(room_id) == 4


def test_success_check_exists_room_by_id():
    room_body = request_room_body()
    room_id = create_room(room_body)
    exists_room = exists_room_by_id(room_id)
    assert exists_room


def test_failure_check_exists_room_by_id():
    exists_room = exists_room_by_id("ABCD")
    assert exists_room is False


def test_success_generate_room_id():
    room_id = generate_room_id()
    assert room_id
    assert len(room_id) == 4


def test_success_change_host_user():
    room_body = request_room_body()
    room_id = create_room(room_body)
    game_start_body = request_start_game_body()
    current_room = json.loads(start_new_game(game_start_body, room_id))
    current_room['game']['selected_users'] = []
    set_content(room_id, current_room)

    new_host_user = request_host_user_body(game_start_body['users'][0])
    current_room = change_host_user(room_id, new_host_user)
    assert_changed_host_user(current_room, new_host_user)


def test_success_change_host_user_and_selected_users():
    room_body = request_room_body()
    previous_host_user = room_body['host_user']

    room_id = create_room(room_body)
    game_start_body = request_start_game_body()
    current_room = json.loads(start_new_game(game_start_body, room_id))

    previous_selected_users = set_selected_users(game_start_body, room_body)
    current_room['game']['selected_users'] = previous_selected_users
    set_content(room_id, current_room)

    new_host_user = request_host_user_body(game_start_body['users'][0])
    current_room = change_host_user(room_id, new_host_user)
    assert_changed_host_user(current_room, new_host_user)

    updated_selected_users = current_room['game']['selected_users']
    assert updated_selected_users
    assert len(updated_selected_users) < len(previous_selected_users)
    assert len([user for user in updated_selected_users
                if user == previous_host_user['uid']]) == 0


def assert_changed_host_user(current_room, new_host_user):
    changed_host_user = current_room['host_user']
    assert changed_host_user
    assert changed_host_user['uid'] == new_host_user['uid']
    assert changed_host_user['nickname'] == new_host_user['nickname']

    current_users = current_room['game']['users']
    assert len(current_users) == 1
    assert len([user for user in current_users
                if user['uid'] == changed_host_user['uid']]) == 0


def set_selected_users(game_start_body, room_body):
    selected_users = [user['uid'] for user in game_start_body['users']]
    selected_users.append(room_body['host_user']['uid'])
    return selected_users


def test_failure_change_host_user_with_room_not_found():
    room_id = '2FV5'

    with pytest.raises(RoomNotFound, match='Room ID {} not found'.format(room_id)):
        change_host_user(room_id, None)


def request_room_body():
    return {'game_type': 2,
            'game_mode': 1,
            'host_user': {
                'uid': DEFAULT_SELECTED_USER_UID,
                'nickname': 'john-doe'
            },
            'total_rounds': DEFAULT_TOTAL_ROUNDS}


def request_start_game_body():
    return {'users': [{'uid': str(uuid.uuid4()), 'nickname': 'bet64'},
                      {'uid': str(uuid.uuid4()), 'nickname': 'avaii'}]}


def request_host_user_body(new_host_user):
    return {
        'uid': new_host_user['uid'],
        'nickname': new_host_user['nickname']
    }
