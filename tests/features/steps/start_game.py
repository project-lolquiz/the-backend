import json
import uuid

from behave import *
from main import default_prefix

APPLICATION_JSON = 'application/json'

use_step_matcher("re")


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


def start_new_game(context):
    return context.world.client.post(default_prefix + '/games/{}/start'.format(context.world.room_id),
                                     data=json.dumps(context.world.request_body),
                                     content_type=APPLICATION_JSON)
