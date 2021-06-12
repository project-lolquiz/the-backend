import os

os.environ['ENV'] = 'qa'

import json
import main
import pytest

from main import default_prefix
from tests.services.games.test_game import request_start_game_body
from tests.services.rooms.test_room import request_room_body
from tests.routes.rooms.test_room import create_game_room

APPLICATION_JSON = 'application/json'
TEXT_HTML_UTF8 = 'text/html; charset=utf-8'


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            yield client


def test_success_create_game_room(client):
    game_room_response = create_game_room(client, request_room_body())

    response_content = json.loads(game_room_response.get_data(as_text=True))
    room_id = response_content['room_id']

    response = client.post(default_prefix + '/games/{}/start'.format(room_id),
                           data=json.dumps(request_start_game_body()),
                           content_type=APPLICATION_JSON)

    assert response
    assert response.content_type == TEXT_HTML_UTF8
    assert response.status_code == 201


def test_failure_create_game_room_with_room_not_found(client):
    room_id = 'DEFG'
    response = client.post(default_prefix + '/games/{}/start'.format(room_id),
                           data=json.dumps(request_start_game_body()),
                           content_type=APPLICATION_JSON)

    assert response
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 404

    response_content = json.loads(response.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' in response_content
    assert response_content['error'] == 'Room ID {} not found'.format(room_id)


def test_failure_create_game_room_with_required_missing_properties(client):
    without_users(client)
    with_users_empty(client)
    without_nickname(client)


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