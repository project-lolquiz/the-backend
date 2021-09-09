import json

from behave import *
from main import default_prefix
from tests.features.steps.game_answer import set_answer
from tests.features.steps.game_question import i_request_a_new_question

APPLICATION_JSON = 'application/json'

use_step_matcher("re")


@when('I request to send the following question x answer combinations for the (\d+) rounds')
def i_request_to_send_the_following_question_x_answer_combinations_for_the_rounds(context, total_rounds):
    for round_num in range(1, int(total_rounds) + 1):
        i_request_a_new_question(context)
        response_content = json.loads(context.world.response_body.get_data(as_text=True))
        selected_user_id = response_content['selected_user_id']

        answer_by_user = [{'uid': row['uid'],
                           'chosen_answer': row['chosen_answer']}
                          for row in context.table if int(row['round']) == round_num]

        selected_user_answer = [answer for answer in answer_by_user if answer['uid'] == selected_user_id][0]
        not_selected_user = [user for user in answer_by_user if user['uid'] != selected_user_id][0]
        not_selected_user['chosen_answer'] = selected_user_answer['chosen_answer']

        answer_body = {'selected_user_id': selected_user_id,
                       'users': answer_by_user}
        context.world.request_body = answer_body
        context.world.response_body = set_answer(context)


@step('The game is ended')
def the_game_is_ended(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'end_game' in response_content
    assert response_content['end_game']


@step('The game is not draw')
def the_game_is_not_draw(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'draw' in response_content
    assert not response_content['draw']


@step('The game is draw')
def the_game_is_draw(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'draw' in response_content
    assert response_content['draw']


@step('I should get a game result score')
def i_should_get_a_game_result_score(context):
    context.world.response_body = get_result_score(context)
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert response_content is not None
    assert 'users' in response_content
    assert len(response_content['users']) > 0


@step('I should get a winner')
def i_should_get_a_winner(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'winner' in response_content
    assert 'nickname' in response_content['winner']
    assert 'total_score' in response_content['winner']
    assert response_content['winner']['total_score'] > 0
    assert 'uid' in response_content['winner']


@step('I should not get a winner')
def i_should_not_get_a_winner(context):
    response_content = json.loads(context.world.response_body.get_data(as_text=True))
    assert 'winner' in response_content
    assert response_content['winner'] is None


def get_result_score(context):
    return context.world.client.get(default_prefix + '/games/{}/results/scores'.format(context.world.room_id),
                                    content_type=APPLICATION_JSON)
