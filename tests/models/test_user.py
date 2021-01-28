from datetime import datetime

from unittest import mock

from models.user import User, find_user_by_uid, update


@mock.patch('models.user.User')
def test_find_user_by_uid(mock_db):
    from_db = mock_db_user(mock_user_registered())
    mock_db.query.filter_by.return_value.first.return_value = from_db

    response = find_user_by_uid(from_db.uid)
    assert_user_registered(response, from_db)


@mock.patch('models.user.User')
def test_failure_find_user_by_uid_with_not_found(mock_db):
    mock_db.query.filter_by.return_value.first.return_value = None
    response = find_user_by_uid('123')
    assert not response


@mock.patch('models.user.db.session')
@mock.patch('models.user.User')
def test_update_user(mock_db, mock_connection):
    from_db = mock_db_user(mock_user_registered())
    mock_db.query.filter_by.return_value.first = from_db

    mock_db.update = None
    mock_connection.commit.return_value = None
    mock_connection.flush.return_value = None

    mock_user = mock_user_registered()
    mock_user['nickname'] = mock_user['nickname'] + '-updated'
    update(mock_user)


@mock.patch('models.user.db.session')
@mock.patch('models.user.User')
def test_add_new(mock_db, mock_connection):
    mock_user = mock_user_registered()
    new_user = User(mock_user['uid'],
                    mock_user['nickname'],
                    mock_user['avatar']['type'],
                    mock_user['avatar']['current'])
    new_user.id = mock_user['id']

    from_db = mock_db_user(mock_user)

    mock_db.add_new.return_value = new_user
    mock_connection.commit.return_value = None
    mock_connection.flush.return_value = None

    response = new_user.add_new()
    assert_user_registered(response, from_db)


def assert_user_registered(response_content, user_registered):
    assert response_content
    assert response_content.id == user_registered.id
    assert response_content.uid == user_registered.uid
    assert response_content.nickname == user_registered.nickname
    assert response_content.created_at
    assert response_content.updated_at
    assert response_content.last_access
    assert response_content.avatar_type == user_registered.avatar_type
    assert response_content.avatar_current_id == user_registered.avatar_current_id


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
