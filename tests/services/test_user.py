from datetime import datetime

from unittest import mock
import pytest

from models.user import User
from services.user_service import add_user, update_user, update_avatar, get_user_by_uid
from components.exception_component import UserAlreadyExists, UserNotFound


@mock.patch('services.user_service.User.add_new')
@mock.patch('services.user_service.find_user_by_uid')
def test_success_add_user(mock_find_user_by_id, mock_add_new):
    mock_find_user_by_id.return_value = None

    user_registered = mock_db_user(mock_user_registered())
    mock_add_new.return_value = user_registered

    content = request_user_body()
    response = add_user(content)
    assert_user_registered(response, user_registered)


@mock.patch('services.user_service.find_user_by_uid')
def test_failure_add_user_with_already_exists(mock_find_user_by_id):
    registered_user = mock_db_user(mock_user_registered())
    mock_find_user_by_id.return_value = registered_user

    with pytest.raises(UserAlreadyExists, match='User {} already registered'.format(registered_user.uid)):
        content = request_user_body()
        add_user(content)


@mock.patch('services.user_service.User.add_new')
@mock.patch('services.user_service.find_user_by_uid')
def test_add_user_without_avatar(mock_find_user_by_id, mock_add_new):
    mock_find_user_by_id.return_value = None

    mock_user = mock_user_registered()
    del mock_user['avatar']
    user_registered = mock_db_user(mock_user)
    mock_add_new.return_value = user_registered

    content = request_user_body()
    response = add_user(content)
    assert_user_registered(response, user_registered)


@mock.patch('services.user_service.db_update')
@mock.patch('services.user_service.find_user_by_uid')
def test_success_update_user(mock_find_user_by_id, mock_update_user):
    mock_user = mock_user_registered()
    registered_user_old = mock_db_user(mock_user)

    new_nickname = 'Nickname updated'

    user_registered = mock_db_user(mock_user_registered())
    user_registered.nickname = 'Nickname updated'

    mock_find_user_by_id.side_effect = [registered_user_old, user_registered]
    mock_update_user.return_value = user_registered

    content = request_user_body()
    content['nickname'] = new_nickname
    response = update_user(content['uid'], content)
    assert_user_registered(response, user_registered)


@mock.patch('services.user_service.find_user_by_uid')
def test_failure_update_user_with_not_found(mock_find_user_by_id):
    registered_user = mock_db_user(mock_user_registered())
    mock_find_user_by_id.return_value = None

    with pytest.raises(UserNotFound, match='User {} not found'.format(registered_user.uid)):
        content = request_user_body()
        update_user(content['uid'], content)


@mock.patch('services.user_service.db_update')
@mock.patch('services.user_service.find_user_by_uid')
def test_success_update_avatar(mock_find_user_by_id, mock_update_user):
    mock_user = mock_user_registered()
    registered_user_old = mock_db_user(mock_user)

    new_avatar_type = '2'
    new_avatar_current = '27'

    user_registered = mock_db_user(mock_user_registered())
    user_registered.avatar_type = new_avatar_type
    user_registered.avatar_current_id = new_avatar_current

    mock_find_user_by_id.side_effect = [registered_user_old, user_registered]
    mock_update_user.return_value = user_registered

    content = request_user_avatar_body()
    uid = content['uid']
    del content['uid']
    content['type'] = new_avatar_type
    content['current'] = new_avatar_current

    response = update_avatar(uid, content)
    assert_user_registered(response, user_registered)


@mock.patch('services.user_service.find_user_by_uid')
def test_failure_update_avatar_with_user_not_found(mock_find_user_by_id):
    registered_user = mock_db_user(mock_user_registered())
    mock_find_user_by_id.return_value = None

    with pytest.raises(UserNotFound, match='User {} not found'.format(registered_user.uid)):
        content = request_user_avatar_body()
        uid = content['uid']
        del content['uid']
        update_avatar(uid, content)


@mock.patch('services.user_service.find_user_by_uid')
def test_success_get_user_by_uid(mock_find_user_by_id):
    registered_user = mock_db_user(mock_user_registered())
    mock_find_user_by_id.return_value = registered_user

    uid = '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'
    response = get_user_by_uid(uid)
    assert_user_registered(response, registered_user)


@mock.patch('services.user_service.find_user_by_uid')
def test_failure_get_user_by_uid_with_not_found(mock_find_user_by_id):
    mock_find_user_by_id.return_value = None

    uid = '4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'
    response = get_user_by_uid(uid)
    assert response is None


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


def mock_db_user(user):
    avatar_type = None
    avatar_current = None
    if 'avatar' in user:
        avatar_type = user['avatar']['type']
        avatar_current = user['avatar']['current']

    db_user = User(user['uid'],
                   user['nickname'],
                   avatar_type,
                   avatar_current)
    now = datetime.now()
    db_user.created_at = now
    db_user.updated_at = now
    db_user.last_access = now
    db_user.id = user['id']
    return db_user


def assert_user_registered(response_content, user_registered, avatar_validate=True):
    assert response_content

    assert 'id' in response_content
    assert response_content['id'] == user_registered.id

    assert 'uid' in response_content
    assert response_content['uid'] == user_registered.uid

    assert 'nickname' in response_content
    assert response_content['nickname'] == user_registered.nickname

    assert 'created_at' in response_content
    assert 'updated_at' in response_content
    assert 'last_access' in response_content

    if avatar_validate:
        assert 'avatar' in response_content
        assert response_content['avatar']

        assert 'type' in response_content['avatar']
        assert response_content['avatar']['type'] == user_registered.avatar_type

        assert 'current' in response_content['avatar']
        assert response_content['avatar']['current'] == user_registered.avatar_current_id
