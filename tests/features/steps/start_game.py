import json
import uuid

from behave import *
from main import default_prefix
from services.redis_service import get_by_key

APPLICATION_JSON = 'application/json'

use_step_matcher("re")


@step("I request to start a new game")
@when("I request to start a new game")
def i_request_to_start_a_new_game(context):
    response = start_new_game(context)
    context.world.response_body = response


@step("a full valid input for start the game")
def a_full_valid_input_for_start_game(context):
    context.world.request_body = {'users': [{'uid': str(uuid.uuid4()), 'nickname': 'bet64'},
                                            {'uid': str(uuid.uuid4()), 'nickname': 'avaii'}]}


@step("an empty response body")
def an_empty_response_body(context):
    assert context.world.response_body.get_data(as_text=True) == ""


@step("an error response body")
def an_error_response_body(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' in response_content


@step('an error message like "([^"]*)"')
def an_error_response_body(context, error_message):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert response_content['error'] == error_message


@step('I should have a "([^"]*)" node on the room')
def i_should_have_value_node_on_the_response_room(context, value):
    current_room = json.loads(get_by_key(context.world.room_id))
    assert value in current_room


@step('I should not have a "([^"]*)" node on the room')
def i_should_not_have_value_node_on_the_response_room(context, value):
    current_room = json.loads(get_by_key(context.world.room_id))
    assert value not in current_room


def start_new_game(context):
    return context.world.client.post(default_prefix + '/games/{}/start'.format(context.world.room_id),
                                     data=json.dumps(context.world.request_body),
                                     content_type=APPLICATION_JSON)
