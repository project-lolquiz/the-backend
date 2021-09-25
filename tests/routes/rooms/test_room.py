import os

os.environ['ENV'] = 'qa'

import json
import main
import pytest

from main import default_prefix
from services.games.game_service import start_new_game
from services.redis_service import set_content
from tests.commons.commons import assert_room_not_found, assert_failure_missing_property
from tests.services.rooms.test_room import request_room_body, request_start_game_body, request_host_user_body

APPLICATION_JSON = 'application/json'


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            yield client


def test_success_create_game_room(client):
    response = create_game_room(client, request_room_body())
    validate_game_room_created(response)


def test_success_check_exists_game_room(client):
    response = create_game_room(client, request_room_body())
    validate_game_room_created(response)

    post_response_content = json.loads(response.get_data(as_text=True))

    get_response = client.get(default_prefix + '/games/rooms/{}'.format(post_response_content['room_id']))
    assert get_response.data
    assert get_response.content_type == APPLICATION_JSON
    assert get_response.status_code == 200

    response_content = json.loads(get_response.get_data(as_text=True))
    assert 'exists' in response_content
    assert response_content['exists']


def test_fail_check_exists_game_room(client):
    response = client.get(default_prefix + '/games/rooms/{}'.format('BCDE'))
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))
    assert 'exists' in response_content
    assert response_content['exists'] is False


def test_success_set_host_user(client):
    game_room_response = create_game_room(client, request_room_body())
    response_content = json.loads(game_room_response.get_data(as_text=True))
    room_id = response_content['room_id']

    game_start_body = request_start_game_body()
    current_room = json.loads(start_new_game(game_start_body, room_id))
    current_room['game']['selected_users'] = []
    set_content(room_id, current_room)

    json_body = request_host_user_body(game_start_body['users'][0])
    response = client.put(default_prefix + '/games/rooms/{}/host_user'.format(room_id),
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)
    assert response
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 204


def test_failure_set_host_user_with_room_not_found(client):
    room_id = 'ZYX1'

    game_start_body = request_start_game_body()
    json_body = request_host_user_body(game_start_body['users'][0])
    response = client.put(default_prefix + '/games/rooms/{}/host_user'.format(room_id),
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)

    assert_room_not_found(response, room_id)


def test_failure_set_host_user_with_required_missing_properties(client):
    without_uid(client)
    without_nickname(client)


def without_uid(client):
    room_id = 'ZYX2'

    game_start_body = request_start_game_body()
    json_body = request_host_user_body(game_start_body['users'][0])
    key_to_remove = 'uid'
    del json_body[key_to_remove]

    response = client.put(default_prefix + '/games/rooms/{}/host_user'.format(room_id),
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, key_to_remove)


def without_nickname(client):
    room_id = 'ZYX3'

    game_start_body = request_start_game_body()
    json_body = request_host_user_body(game_start_body['users'][0])
    key_to_remove = 'nickname'
    del json_body[key_to_remove]

    response = client.put(default_prefix + '/games/rooms/{}/host_user'.format(room_id),
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, key_to_remove)


def create_game_room(client, body):
    response = client.post(default_prefix + '/games/rooms',
                           data=json.dumps(body),
                           content_type=APPLICATION_JSON)
    return response


def validate_game_room_created(response):
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 201

    response_content = json.loads(response.get_data(as_text=True))
    assert 'room_id' in response_content
    assert len(response_content['room_id']) == 4
