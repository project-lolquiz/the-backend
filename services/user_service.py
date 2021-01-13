from flask import jsonify
import json

from models.user import User, update as db_update, find_user_by_uid


# TODO: VERIFICAR A EXISTENCIA DO UID ANTES DE CRIAR
def add_user(content):
    user = json.loads(json.dumps(content))
    new_user = User(user['uid'], user['nickname'], user['avatar']['type'], user['avatar']['current'])
    new_user.add_new()
    return from_model_to_dict(new_user)


def update_user(uid, content):
    current_user = json.loads(json.dumps(content))
    current_user['uid'] = uid
    return update(current_user)


def update_avatar(uid, content):
    avatar = json.loads(json.dumps(content))
    user = find_user_by_uid(uid)
    current_user = from_model_to_dict(user)
    current_user['avatar']['type'] = avatar['type']
    current_user['avatar']['current'] = avatar['current']
    return update(current_user)


def update(user):
    db_update(user)
    return get_user_by_uid(user['uid'])


def get_user_by_uid(uid):
    return from_model_to_dict(find_user_by_uid(uid))


def from_model_to_dict(user):
    if user is None:
        return {}
    return {'id': user.id,
            'uid': user.uid,
            'nickname': user.nickname,
            'avatar':
                {'type': user.avatar_type, 'current': user.avatar_current_id},
            'created_at': str(user.created_at),
            'updated_at': str(user.updated_at),
            'last_access': str(user.last_access)}
