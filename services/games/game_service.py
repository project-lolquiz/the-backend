import json

from components.exception_component import RoomNotFound
from services.redis_service import set_content, get_by_key
from services.rooms.room_service import exists_room_by_id


def start_new_game(content, room_id):
    room_data = json.loads(json.dumps(content))

    if not exists_room_by_id(room_id):
        raise RoomNotFound('Room ID {} not found'.format(room_id))

    current_room = json.loads(get_by_key(room_id))
    current_room['game'] = room_data

    set_content(room_id, current_room)
    return get_by_key(room_id)
