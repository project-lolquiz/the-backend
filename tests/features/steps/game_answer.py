import json

from behave import *
from main import default_prefix

APPLICATION_JSON = 'application/json'

use_step_matcher("re")


@when('I request to send the following answers')
def i_request_to_send_the_answers_with_user_choosing_the_right_choice(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    selected_user_id = response_content['selected_user_id']

    users = []
    for row in context.table:
        user = {'uid': row['uid'],
                'chosen_answer': row['chosen_answer']}
        if selected_user_id != row['uid'] and len([right_answer for right_answer in users
                                                   if right_answer['chosen_answer']]) == 0:
            user['chosen_answer'] = selected_user_id
        users.append(user)

    answer_body = {'selected_user_id': selected_user_id,
                   'users': set_only_one_user_with_right_answer(users, selected_user_id)}
    context.world.request_body = answer_body
    context.world.response_body = set_answer(context)


def set_only_one_user_with_right_answer(users, selected_user_id):
    user_with_right_answer = [user for user in users if user['chosen_answer'] == selected_user_id]
    if len(user_with_right_answer) == 1:
        return users

    for user in users:
        if user['uid'] != selected_user_id:
            user['chosen_answer'] = selected_user_id
            break

    return users


@when('I request to send all the answers with the right choice')
def i_request_to_send_all_the_answers_with_the_right_choice(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    selected_user_id = response_content['selected_user_id']

    users = []
    for row in context.table:
        users.append({'uid': row['uid'],
                      'chosen_answer': selected_user_id})

    answer_body = {'selected_user_id': selected_user_id,
                   'users': users}
    context.world.request_body = answer_body
    context.world.response_body = set_answer(context)


@step('I should get a valid answer response')
def i_should_get_a_valid_answer_response(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'draw' in response_content
    assert 'end_game' in response_content
    assert 'users' in response_content
    assert len(response_content['users']) > 0


@step('Only one user should answered right')
def only_one_user_should_answered_right(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    answers = response_content['users']
    right_answer = [answer for answer in answers if answer['correct_answer']]
    assert len(right_answer) == 1


@step('All users should answered right')
def all_users_should_answered_right(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    answers = response_content['users']
    user_answers = [row['uid'] for row in context.table]
    right_answers = [answer for answer in answers if answer['correct_answer']]
    assert len(right_answers) == (len(user_answers) - 1)


def set_answer(context):
    return context.world.client.post(default_prefix + '/games/{}/questions/answers'.format(context.world.room_id),
                                     data=json.dumps(context.world.request_body),
                                     content_type=APPLICATION_JSON)
