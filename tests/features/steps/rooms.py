import os
import uuid

os.environ['ENV'] = 'qa'

import json
import main

from aloe import before, step, world
from main import default_prefix

APPLICATION_JSON = 'application/json'


@before.each_example
def before_all(*args):
    world.client = main.app.test_client()
    world.room_id = None


@step(r'a full valid input for new room')
def a_full_valid_input(self):
    world.request_body = {'game_type': 10,
                          'game_mode': 11,
                          'host_user': {
                              'uid': str(uuid.uuid4()),
                              'nickname': 'john-doe'
                          },
                          'total_rounds': 10}


@step(r'I request to create a new room')
def i_request_to_create_a_new_room(self):
    response = create_new_game_room()
    world.response_body = response


@step(r'I should get a (\d+) http response code')
def i_should_get_a_http_response_code(self, http_status_code):
    assert world.response_body.status_code == int(http_status_code)


@step(r'I should get a new room code')
def i_should_get_a_new_room_code(self):
    response_content = json.loads(world.response_body.get_data(as_text=True))
    assert 'room_id' in response_content
    assert len(response_content['room_id']) == 4


@step(r'a room code')
def a_room_code(self):
    a_full_valid_input(self)
    i_request_to_create_a_new_room(self)
    response_content = json.loads(world.response_body.get_data(as_text=True))
    world.room_id = response_content['room_id']


@step(r'a room with id "([^"]*)"')
def a_room_with_id(self, room_code):
    world.room_id = room_code


@step(r'I request to check the existence of this room code')
def i_request_to_check_existence_room_code(self):
    world.response_body = world.client.get(default_prefix + '/games/rooms/{}'.format(world.room_id))


@step(r'I should get the the exists response as "([^"]*)"')
def i_request_to_check_existence_room_code(self, exists_room_code):
    response_content = json.loads(world.response_body.get_data(as_text=True))
    assert 'exists' in response_content
    assert str(response_content['exists']) == exists_room_code


def create_new_game_room():
    return world.client.post(default_prefix + '/games/rooms',
                             data=json.dumps(world.request_body),
                             content_type=APPLICATION_JSON)
