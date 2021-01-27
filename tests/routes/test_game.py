import json

from unittest import mock
import pytest

import main
from main import default_prefix

APPLICATION_JSON = 'application/json'

@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            yield client


@mock.patch('routes.game_route.get_all_types')
def test_game_types(mock_db_service, client):
    list_db_value = generate_mock_db_values()
    mock_db_service.return_value = list_db_value

    response = client.get(default_prefix + '/games/types')
    assert_response(response, list_db_value)


@mock.patch('routes.game_route.get_all_modes')
def test_game_modes(mock_db_service, client):
    list_db_value = generate_mock_db_values()
    mock_db_service.return_value = list_db_value

    response = client.get(default_prefix + '/games/modes')
    assert_response(response, list_db_value)


def generate_mock_db_values():
    return [{'id': index,
             'name': 'Name_' + str(index),
             'description': 'Description_' + str(index)}
            for index in range(1, 4)]


def assert_response(response, list_db_value):
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))
    assert len(response_content) == len(list_db_value)

    for index in range(0, len(list_db_value)):
        content = response_content[index]
        from_db = list_db_value[index]
        assert 'id' in content
        assert 'name' in content
        assert 'description' in content
        assert content['id'] == from_db['id']
        assert content['name'] == from_db['name']
        assert content['description'] == from_db['description']