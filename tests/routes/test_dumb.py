import json

from unittest import mock
import pytest

import main
from main import default_prefix

APPLICATION_JSON = 'application/json'
TEXT_HTML_UTF8 = 'text/html; charset=utf-8'


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            yield client


@mock.patch('routes.dumb_route.get_by_key')
def test_redis_get_by_key(mock_redis_service, client):
    mock_redis_service.return_value = "{\"value\": \"redis-value\"}"

    response = client.get(default_prefix + '/redis-get-by-key/redis-key')
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))
    assert response_content['key'] == 'redis-key'
    assert response_content['value']


@mock.patch('routes.dumb_route.get_by_key')
def test_failure_redis_get_by_key(mock_redis_service, client):
    mock_redis_service.return_value = "key-value"

    response = client.get(default_prefix + '/redis-get-by-key/redis-key')
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 404

    response_content = json.loads(response.get_data(as_text=True))
    assert response_content
    assert response_content['error'] == 'Key redis-key not found'
    assert response_content['timestamp']


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


@mock.patch('routes.dumb_route.from_redis')
def test_redis_get_all(mock_redis_service, client):
    redis_content = [{'key' + str(index): 'value_' + str(index)} for index in range(1, 5)]

    mock_redis_service.return_value = redis_content

    response = client.get(default_prefix + '/redis-get-all')
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))
    assert len(response_content) == 4

    for index in range(1, len(response_content) + 1):
        content = response_content[index - 1]
        assert 'key' + str(index) in content
        assert content['key' + str(index)] == 'value_' + str(index)


@mock.patch('routes.dumb_route.delete_all')
def test_redis_delete_all(mock_redis_service, client):
    mock_redis_service.return_value = None

    response = client.delete(default_prefix + '/redis-delete-all')
    assert not response.data
    assert response.status_code == 204
    assert response.content_type == TEXT_HTML_UTF8


@mock.patch('routes.dumb_route.delete_by_key')
def test_redis_delete_by_key(mock_redis_service, client):
    mock_redis_service.return_value = None

    response = client.delete(default_prefix + '/redis-delete-by-key/a-key')
    assert not response.data
    assert response.status_code == 204
    assert response.content_type == TEXT_HTML_UTF8


@mock.patch('routes.dumb_route.into_db')
def test_db_add(mock_db_service, client):
    mock_db_service.return_value = None

    json_body = {'value': 'Adding new item'}
    response = client.post(default_prefix + '/db-add',
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 201

    response_content = json.loads(response.get_data(as_text=True))
    assert 'value' in response_content
    assert response_content['value'] == 'Adding new item'


@mock.patch('routes.dumb_route.get_by_id')
def test_db_get_by_id(mock_db_service, client):
    dict_db_value = {'id': 1, 'value': 'The new item'}
    mock_db_service.return_value = dict_db_value

    response = client.get(default_prefix + '/db-get-by-id/'
                          + str(dict_db_value['id']))
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))
    assert 'id' in response_content
    assert 'value' in response_content
    assert response_content['id'] == dict_db_value['id']
    assert response_content['value'] == dict_db_value['value']


@mock.patch('routes.dumb_route.from_db')
def test_db_get_all(mock_db_service, client):
    list_db_value = [{'id': index, 'value': 'Item_' + str(index)}
                     for index in range(1, 5)]
    mock_db_service.return_value = list_db_value

    response = client.get(default_prefix + '/db-get-all')
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 200

    response_content = json.loads(response.get_data(as_text=True))
    assert len(response_content) == len(list_db_value)

    for index in range(0, len(list_db_value)):
        content = response_content[index]
        from_db = list_db_value[index]
        assert 'id' in content
        assert 'value' in content
        assert content['id'] == from_db['id']
        assert content['value'] == from_db['value']