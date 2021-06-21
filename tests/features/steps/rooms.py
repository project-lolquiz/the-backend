import json
import uuid

from behave import *
from main import default_prefix

APPLICATION_JSON = 'application/json'

use_step_matcher("re")


@given("a full valid input for new room")
def a_full_valid_input(context):
    context.world.request_body = {'game_type': 10,
                                  'game_mode': 11,
                                  'host_user': {
                                      'uid': str(uuid.uuid4()),
                                      'nickname': 'john-doe'
                                  },
                                  'total_rounds': 10}


@when("I request to create a new room")
def i_request_to_create_a_new_room(context):
    response = create_new_game_room(context)
    context.world.response_body = response


@then("I should get a (\d+) http response code")
def i_should_get_a_http_response_code(context, http_status_code):
    assert context.world.response_body.status_code == int(http_status_code)


@step("I should get a new room code")
def i_should_get_a_new_room_code(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'room_id' in response_content
    assert len(response_content['room_id']) == 4


@given('a room code')
def a_room_code(context):
    a_full_valid_input(context)
    i_request_to_create_a_new_room(context)
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    context.world.room_id = response_content['room_id']


@when('I request to check the existence of this room code')
def i_request_to_check_existence_room_code(context):
    context.world.response_body = context.world.client.get(default_prefix + '/games/rooms/{}'
                                                           .format(context.world.room_id))


@step('I should get the the exists response as "([^"]*)"')
def i_request_to_check_existence_room_code(context, exists_room_code):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'exists' in response_content
    assert str(response_content['exists']) == exists_room_code


@given(r'a room with id "([^"]*)"')
def a_room_with_id(context, room_code):
    context.world.room_id = room_code


def create_new_game_room(context):
    return context.world.client.post(default_prefix + '/games/rooms',
                                     data=json.dumps(context.world.request_body),
                                     content_type=APPLICATION_JSON)
