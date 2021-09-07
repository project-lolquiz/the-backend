import json

from behave import *
from main import default_prefix
from tests.features.steps.rooms import create_new_game_room
from tests.features.steps.start_game import start_new_game

APPLICATION_JSON = 'application/json'

use_step_matcher("re")


@given("I request to create a new room with")
def i_request_to_create_a_new_room_with(context):
    new_game_room = {}
    for row in context.table:
        new_game_room['game_type'] = int(row['game_type'])
        new_game_room['game_mode'] = int(row['game_mode'])
        new_game_room['host_user'] = {'uid': row['host_user_uid'],
                                      'nickname': row['host_user_nickname']}
        new_game_room['total_rounds'] = int(row['total_rounds'])
    context.world.request_body = new_game_room
    context.world.response_body = create_new_game_room(context)


@step("I request to start a new game with users")
def i_request_to_start_a_new_game_with_users(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    context.world.room_id = response_content['room_id']

    users = []
    for row in context.table:
        users.append({'uid': row['uid'], 'nickname': row['nickname']})

    context.world.request_body = {'users': users}
    start_new_game(context)


@step("I request a new question")
@when("I request a new question")
def i_request_a_new_question(context):
    context.world.response_body = get_question(context)


@step("I should get a valid question")
def i_should_get_a_valid_question(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'draw' in response_content
    assert 'options' in response_content
    assert len(response_content['options']) > 0
    assert 'round' in response_content
    assert 'current' in response_content['round']
    assert 'total' in response_content['round']
    assert 'selected_user_id' in response_content
    assert 'title' in response_content


def get_question(context):
    return context.world.client.get(default_prefix + '/games/{}/questions'.format(context.world.room_id),
                                    content_type=APPLICATION_JSON)
