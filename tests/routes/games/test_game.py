import os

os.environ['ENV'] = 'qa'

import json
import main
import pytest

from main import default_prefix
from services.games.questions.answers.answer_service import set_answer
from services.games.game_service import start_new_game
from tests.services.games.test_game import request_start_game_body
from tests.services.rooms.test_room import request_room_body, DEFAULT_SELECTED_USER_UID
from tests.routes.rooms.test_room import create_game_room
from tests.services.games.test_game import create_game_room as create_game_room_from_service
from tests.services.games.questions.answers.test_answer import create_answer_body

APPLICATION_JSON = 'application/json'
TEXT_HTML_UTF8 = 'text/html; charset=utf-8'


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            yield client


def test_success_start_new_game(client):
    game_room_response = create_game_room(client, request_room_body())

    response_content = json.loads(game_room_response.get_data(as_text=True))
    room_id = response_content['room_id']

    response = client.post(default_prefix + '/games/{}/start'.format(room_id),
                           data=json.dumps(request_start_game_body()),
                           content_type=APPLICATION_JSON)

    assert response
    assert response.content_type == TEXT_HTML_UTF8
    assert response.status_code == 201


def test_failure_start_new_game_with_room_not_found(client):
    room_id = 'DEFG'
    response = client.post(default_prefix + '/games/{}/start'.format(room_id),
                           data=json.dumps(request_start_game_body()),
                           content_type=APPLICATION_JSON)
    assert_room_not_found(response, room_id)


def test_failure_start_new_game_with_required_missing_properties(client):
    without_users(client)
    with_users_empty(client)
    without_nickname(client)


def test_success_get_game_question(client):
    room_id = create_game_room_from_service()
    body = request_start_game_body()
    start_new_game(body, room_id)

    response = client.get(default_prefix + '/games/{}/questions'.format(room_id),
                          content_type=APPLICATION_JSON)
    assert response is not None
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))

    assert 'title' in response_content
    assert 'options' in response_content
    assert len(response_content['options']) > 0
    assert 'round' in response_content
    assert 'selected_user_id' in response_content
    assert 'draw' in response_content


def test_failure_get_game_question_with_room_not_found(client):
    room_id = 'DEFG'

    response = client.get(default_prefix + '/games/{}/questions'.format(room_id),
                          content_type=APPLICATION_JSON)
    assert_room_not_found(response, room_id)


def test_success_set_answer(client):
    room_id = create_game_room_from_service()
    body = request_start_game_body()
    start_new_game(body, room_id)
    body = create_answer_body()
    body['users'][0]['chosen_answer'] = DEFAULT_SELECTED_USER_UID

    response = client.post(default_prefix + '/games/{}/questions/answers'.format(room_id),
                           data=json.dumps(body),
                           content_type=APPLICATION_JSON)

    assert response is not None
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 201

    response_content = json.loads(response.get_data(as_text=True))

    assert 'draw' in response_content
    assert 'end_game' in response_content
    assert 'users' in response_content
    assert len(response_content['users']) > 0


def test_failure_set_answer_with_room_not_found(client):
    room_id = 'D13G'
    body = create_answer_body()
    body['users'][0]['chosen_answer'] = DEFAULT_SELECTED_USER_UID

    response = client.post(default_prefix + '/games/{}/questions/answers'.format(room_id),
                           data=json.dumps(body),
                           content_type=APPLICATION_JSON)
    assert_room_not_found(response, room_id)


def test_failure_set_answer_with_required_missing_properties(client):
    without_selected_user_id(client)
    without_user_answer(client)


def test_success_game_result_score(client):
    room_id = create_game_room_from_service()
    body = request_start_game_body()
    start_new_game(body, room_id)
    body = create_answer_body()
    body['users'][0]['chosen_answer'] = DEFAULT_SELECTED_USER_UID
    set_answer(room_id, body)

    response = client.get(default_prefix + '/games/{}/results/scores'.format(room_id),
                          content_type=APPLICATION_JSON)
    assert response is not None
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))

    assert 'users' in response_content
    assert len(response_content['users']) > 0
    assert 'winner' in response_content


def test_failure_game_result_score_with_room_not_found(client):
    room_id = 'AEFG'

    response = client.get(default_prefix + '/games/{}/results/scores'.format(room_id),
                          content_type=APPLICATION_JSON)
    assert_room_not_found(response, room_id)


def without_users(client):
    game_room_response = create_game_room(client, request_room_body())

    response_content = json.loads(game_room_response.get_data(as_text=True))
    room_id = response_content['room_id']

    key_to_remove = 'users'
    json_body = request_start_game_body()
    del json_body[key_to_remove]

    response = client.post(default_prefix + '/games/{}/start'.format(room_id),
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, key_to_remove)


def with_users_empty(client):
    game_room_response = create_game_room(client, request_room_body())

    response_content = json.loads(game_room_response.get_data(as_text=True))
    room_id = response_content['room_id']

    json_body = {'users': [{}]}

    response = client.post(default_prefix + '/games/{}/start'.format(room_id),
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, 'uid')


def without_nickname(client):
    game_room_response = create_game_room(client, request_room_body())

    response_content = json.loads(game_room_response.get_data(as_text=True))
    room_id = response_content['room_id']

    json_body = {'users': [{'uid': '8852c5af-a6e5-4fad-9022-3d10ed111a30'}]}

    response = client.post(default_prefix + '/games/{}/start'.format(room_id),
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, 'nickname')


def assert_failure_missing_property(response, missing_property):
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 400

    response_content = json.loads(response.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' not in response_content
    assert response_content['error'] == '\'{}\' is a required property'.format(missing_property)


def assert_room_not_found(response, room_id):
    assert response
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 404

    response_content = json.loads(response.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' in response_content
    assert response_content['error'] == 'Room ID {} not found'.format(room_id)


def without_selected_user_id(client):
    room_id = create_game_room_from_service()
    body = request_start_game_body()
    start_new_game(body, room_id)
    body = create_answer_body()

    key_to_remove = 'selected_user_id'
    del body[key_to_remove]

    response = client.post(default_prefix + '/games/{}/questions/answers'.format(room_id),
                           data=json.dumps(body),
                           content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, key_to_remove)


def without_user_answer(client):
    room_id = create_game_room_from_service()
    body = request_start_game_body()
    start_new_game(body, room_id)
    body = create_answer_body()

    key_to_remove = 'users'
    del body[key_to_remove]

    response = client.post(default_prefix + '/games/{}/questions/answers'.format(room_id),
                           data=json.dumps(body),
                           content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, key_to_remove)