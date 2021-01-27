from datetime import datetime

import json

from unittest import mock
import pytest

import main
from components.exception_component import UserAlreadyExists, UserNotFound
from main import default_prefix

APPLICATION_JSON = 'application/json'
TEXT_HTML_UTF8 = 'text/html; charset=utf-8'


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


@mock.patch('routes.user_route.add_user')
def test_success_user_register_without_avatar(mock_db_service, client):
    user_registered = mock_user_registered()
    del user_registered['avatar']
    mock_db_service.return_value = user_registered

    json_body = request_user_body()
    response = client.post(default_prefix + '/users/register',
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 201

    response_content = json.loads(response.get_data(as_text=True))
    assert_user_registered(response_content, json_body, False)


@mock.patch('routes.user_route.add_user')
def test_failure_user_register_with_already_exists(mock_db_service, client):
    default_uid = '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'
    error_message = 'User {} already registered'.format(default_uid)
    mock_db_service.side_effect = UserAlreadyExists(error_message)

    json_body = request_user_body()
    response = client.post(default_prefix + '/users/register',
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 400

    response_content = json.loads(response.get_data(as_text=True))
    assert_failure_user_register(response_content, error_message)


def test_failure_user_register_with_required_missing_properties(client):
    user_without_uid(client)
    user_without_nickname(client)


def user_without_uid(client):
    json_body = request_user_body()
    key_to_remove = 'uid'
    del json_body[key_to_remove]
    response = client.post(default_prefix + '/users/register',
                           data=json.dumps(json_body),
                           content_type=APPLICATION_JSON)
    assert_failure_missing_property(response, key_to_remove)


def user_without_nickname(client, operation='POST'):
    json_body = request_user_body()
    key_to_remove = 'nickname'
    del json_body[key_to_remove]

    if operation == 'POST':
        response = client.post(default_prefix + '/users/register',
                               data=json.dumps(json_body),
                               content_type=APPLICATION_JSON)
    else:
        uid = json_body['uid']
        del json_body['uid']
        response = client.put(default_prefix + '/users/' + uid,
                              data=json.dumps(json_body),
                              content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, key_to_remove)


def user_without_avatar_property(client, avatar_property='avatar', full_body=True):
    avatar_context = ''
    if full_body:
        json_body = request_user_body()
    else:
        json_body = request_user_avatar_body()
        avatar_context = '/avatar'

    if avatar_property == 'avatar':
        del json_body[avatar_property]
    elif full_body:
        del json_body['avatar'][avatar_property]
    else:
        del json_body[avatar_property]

    uid = json_body['uid']
    del json_body['uid']
    response = client.put(default_prefix + '/users/' + uid + avatar_context,
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)

    assert_failure_missing_property(response, avatar_property)


@mock.patch('routes.user_route.update_user')
def test_success_user_update(mock_db_service, client):
    user_registered = mock_user_registered()
    mock_db_service.return_value = user_registered

    json_body = request_user_body()
    uid = json_body['uid']
    del json_body['uid']
    response = client.put(default_prefix + '/users/' + uid,
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)
    assert not response.data
    assert response.content_type == TEXT_HTML_UTF8
    assert response.status_code == 204


@mock.patch('routes.user_route.update_user')
def test_failure_user_update_with_not_found(mock_db_service, client):
    default_uid = '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'
    error_message = 'User {} not found'.format(default_uid)
    mock_db_service.side_effect = UserNotFound(error_message)

    json_body = request_user_body()
    uid = json_body['uid']
    del json_body['uid']
    response = client.put(default_prefix + '/users/' + uid,
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 404

    response_content = json.loads(response.get_data(as_text=True))
    assert_failure_user_register(response_content, error_message)


def test_failure_user_update_with_required_missing_properties(client):
    user_without_nickname(client, 'PUT')
    user_without_avatar_property(client)
    user_without_avatar_property(client, 'type')
    user_without_avatar_property(client, 'current')


@mock.patch('routes.user_route.update_avatar')
def test_success_user_avatar_update(mock_db_service, client):
    user_registered = mock_user_registered()
    mock_db_service.return_value = user_registered

    json_body = request_user_avatar_body()
    uid = json_body['uid']
    del json_body['uid']
    response = client.put(default_prefix + '/users/' + uid + '/avatar',
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)
    assert not response.data
    assert response.content_type == TEXT_HTML_UTF8
    assert response.status_code == 204


@mock.patch('routes.user_route.update_avatar')
def test_failure_user_avatar_update_with_not_found(mock_db_service, client):
    default_uid = '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'
    error_message = 'User {} not found'.format(default_uid)
    mock_db_service.side_effect = UserNotFound(error_message)

    json_body = request_user_avatar_body()
    uid = json_body['uid']
    del json_body['uid']
    response = client.put(default_prefix + '/users/' + uid + '/avatar',
                          data=json.dumps(json_body),
                          content_type=APPLICATION_JSON)
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 404

    response_content = json.loads(response.get_data(as_text=True))
    assert_failure_user_register(response_content, error_message)


def test_failure_user_avatar_update_with_required_missing_properties(client):
    user_without_avatar_property(client, 'type', False)
    user_without_avatar_property(client, 'current', False)


def assert_user_registered(response_content, json_body, avatar_validate=True):
    assert 'id' in response_content
    assert 'uid' in response_content
    assert 'nickname' in response_content
    assert 'created_at' in response_content
    assert 'updated_at' in response_content
    assert 'last_access' in response_content
    assert response_content['uid'] == json_body['uid']

    if avatar_validate:
        assert 'avatar' in response_content
        assert 'type' in response_content['avatar']
        assert 'current' in response_content['avatar']
        assert response_content['avatar']
        assert response_content['avatar']['type']
        assert response_content['avatar']['current']
    else:
        assert 'avatar' not in response_content


def assert_failure_user_register(response_content, error_message):
    assert 'error' in response_content
    assert 'timestamp' in response_content
    assert response_content['error'] == error_message


def assert_failure_missing_property(response, missing_property):
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 400

    response_content = json.loads(response.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' not in response_content
    assert response_content['error'] == '\'{}\' is a required property'.format(missing_property)


def request_user_body():
    return {'uid': '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069',
            'nickname': 'john-doe',
            'avatar':
                {'type': '1',
                 'current': '10'}}


def request_user_avatar_body():
    return {'uid': '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069',
            'type': '1',
            'current': '10'}


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
