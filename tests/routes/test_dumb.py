import json

from unittest import mock
import pytest

import main
from main import default_prefix

APPLICATION_JSON = "application/json"


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            yield client


@mock.patch('routes.dumb_route.get_by_key')
def test_redis_get_by_key(mock_redis_service, client):
    mock_redis_service.return_value = 'redis-value'

    response = client.get(default_prefix + '/redis-get-by-key/redis-key')
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))
    assert response_content['key'] == 'redis-key'
    assert response_content['value'] == 'redis-value'


@mock.patch('routes.dumb_route.into_redis')
def test_redis_add(mock_redis_service, client):
    mock_redis_service.return_value = None

    json_body = {'key': 'the-key', 'value': 'the-value', 'expires_in': 10}
    response = client.post(default_prefix + '/redis-add',
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 201

    response_content = json.loads(response.get_data(as_text=True))
    assert response_content['key'] == 'the-key'
    assert response_content['value'] == 'the-value'
    assert response_content['expires_in'] == 10
