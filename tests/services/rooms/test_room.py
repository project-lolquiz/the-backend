import os

os.environ['ENV'] = 'qa'

from services.rooms.room_service import create_room


def test_success_create_room():
    room_body = request_room_body()
    room_id = create_room(room_body)
    assert room_id
    assert len(room_id) == 4


def request_room_body():
    return {'game_type': 10,
            'game_mode': 11,
            'host_user': {
                'uid': '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069',
                'nickname': 'john-doe'
            },
            'total_rounds': 10}