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


@step(r'a full valid input for new room')
def a_full_valid_input(self):
    world.request_body = {'game_type': 10,
                          'game_mode': 11,
                          'host_user': {
                              'uid': str(uuid.uuid4()),
                              'nickname': 'john-doe'
                          },
                          'total_rounds': 10}


@step(r'I request to crate a new room')
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


def create_new_game_room():
    return world.client.post(default_prefix + '/games/rooms',
                             data=json.dumps(world.request_body),
                             content_type=APPLICATION_JSON)
