from datetime import datetime

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


@mock.patch('routes.user_route.add_user')
def test_success_user_register(mock_db_service, client):
    user_registered = mock_user_registered()
    mock_db_service.return_value = user_registered

    json_body = request_user_body()
    response = client.post(default_prefix + '/users/register',
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 201

    response_content = json.loads(response.get_data(as_text=True))
    assert_user_registered(response_content, json_body)


def assert_user_registered(response_content, json_body):
    assert 'id' in response_content
    assert 'uid' in response_content
    assert 'nickname' in response_content
    assert 'avatar' in response_content
    assert 'type' in response_content['avatar']
    assert 'current' in response_content['avatar']
    assert 'created_at' in response_content
    assert 'updated_at' in response_content
    assert 'last_access' in response_content
    assert response_content['uid'] == json_body['uid']
    assert response_content['avatar']
    assert response_content['avatar']['type']
    assert response_content['avatar']['current']


def request_user_body():
    return {'uid': '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069',
            'nickname': 'john-doe',
            'avatar':
                {'type': '1',
                 'current': '10'}}


def mock_user_registered():
    now = datetime.now()
    return {'id': 1,
            'uid': '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069',
            'nickname': 'john-doe',
            'avatar':
                {'type': '1',
                 'current': '10'},
            'created_at': str(now),
            'updated_at': str(now),
            'last_access': str(now)}
