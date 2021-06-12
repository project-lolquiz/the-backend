import os

os.environ['ENV'] = 'qa'

import json
import main
import pytest

from main import default_prefix
from tests.services.rooms.test_room import request_room_body

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