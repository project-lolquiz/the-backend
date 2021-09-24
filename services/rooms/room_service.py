import json
import random
import string

from components.exception_component import RoomNotFound
from services.redis_service import set_content, get_by_key


def create_room(content):
    room_data = json.loads(json.dumps(content))
    room_id = generate_room_id()
    room_data['room_id'] = room_id
    set_content(room_id, room_data)
    return room_id


def exists_room_by_id(room_id):
    return get_by_key(room_id) is not None


def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))


def change_host_user(room_id, content):
    if not exists_room_by_id(room_id):
        raise RoomNotFound('Room ID {} not found'.format(room_id))

    host_user = json.loads(json.dumps(content))
    current_room = json.loads(get_by_key(room_id))

    current_room = remove_host_user_from_users(current_room, host_user)
    current_room = remove_current_host_user_from_selected_users(current_room)
    current_room = set_host_user(current_room, host_user)
    set_content(room_id, current_room)

    return current_room


def remove_host_user_from_users(current_room, host_user):
    current_users = current_room['game']['users']
    users = [user for user in current_users if user['uid'] != host_user['uid']]
    current_room['game']['users'] = users
    return current_room


def remove_current_host_user_from_selected_users(current_room):
    current_selected_users = current_room['game']['selected_users']
    host_user = current_room['host_user']
    selected_users = [user for user in current_selected_users if user != host_user['uid']]
    current_room['game']['selected_users'] = selected_users
    return current_room


def set_host_user(current_room, host_user):
    current_room['host_user'] = host_user
    return current_room
