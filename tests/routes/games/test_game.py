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