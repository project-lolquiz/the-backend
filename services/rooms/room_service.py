import json
import random
import string

from services.redis_service import set_content


def create_room(content):
    room_data = json.loads(json.dumps(content))
    room_id = generate_room_id()
    room_data['room_id'] = room_id
    set_content(room_id, room_data)
    return room_id


def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
