import json

from behave import *
from main import default_prefix
from services.redis_service import get_by_key, set_content
from services.rooms.room_service import has_game_users, is_game_started, has_selected_users

APPLICATION_JSON = 'application/json'

use_step_matcher("re")


@step("there is a selected users list")
def there_is_a_selected_users_list(context):
    current_room = json.loads(get_by_key(context.world.room_id))
    current_room['game']['selected_users'] = []
    set_content(context.world.room_id, current_room)


@step("there is a selected users list with")
def there_is_a_selected_users_list_with(context):
    selected_users = []
    for row in context.table:
        selected_users.append(row['uid'])

    current_room = json.loads(get_by_key(context.world.room_id))
    current_room['game']['selected_users'] = selected_users
    set_content(context.world.room_id, current_room)


@when("I request to set the new host user as")
def i_request_to_set_the_new_host_user_as(context):
    for row in context.table:
        context.world.request_body = {'uid': row['uid'],
                                      'nickname': row['nickname']}
    context.world.response_body = set_host_user(context)


@step("there will be only (\d+) users in the game")
def there_will_be_only_users_in_the_game(context, total_users):
    current_room = json.loads(get_by_key(context.world.room_id))

    users = []
    if has_game_users(current_room):
        current_game = current_room['game']
        users = current_game['users']

    host_user = current_room['host_user']
    users.append(host_user)

    assert len(users) == int(total_users)


@step("there will be only (\d+) users in the selected users list")
def there_will_be_only_users_in_the_selected_users_list(context, total_users):
    current_room = json.loads(get_by_key(context.world.room_id))

    selected_users = []
    if is_game_started(current_room):
        current_game = current_room['game']
        selected_users = current_game['selected_users']

    assert len(selected_users) == int(total_users)


@step("there will have no selected users list")
def there_will_have_no_selected_users_list(context):
    current_room = json.loads(get_by_key(context.world.room_id))
    assert not has_selected_users(current_room)


@step("the host user is not")
def the_host_user_is_not(context):
    previous_host_user = {}
    for row in context.table:
        previous_host_user = {'uid': row['uid'],
                              'nickname': row['nickname']}

    current_room = json.loads(get_by_key(context.world.room_id))
    host_user = current_room['host_user']

    assert previous_host_user['uid'] != host_user['uid']
    assert previous_host_user['nickname'] != host_user['nickname']


def set_host_user(context):
    return context.world.client.put(default_prefix + '/games/rooms/{}/host_user'.format(context.world.room_id),
                                    data=json.dumps(context.world.request_body),
                                    content_type=APPLICATION_JSON)
