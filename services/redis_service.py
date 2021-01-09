import json

from app import get_redis_connection

_redis = get_redis_connection()


def add(content):
    expires_in = content['expires_in']
    if expires_in is None:
        expires_in = 10
    _json = json.dumps(content)
    _redis.set(content['key'], _json, expires_in)


def get_by_key(key):
    return _redis.get(key)


def get_all():
    _redis.set('full stack', 'python')
    _redis.set('version', '3')
    _redis.set('framework', 'flask')
    keys = _redis.keys()
    return {keys[index]: _redis.get(keys[index]) for index in range(0, len(keys))}


def delete_all():
    for key in _redis.keys():
        delete_by_key(key)


def delete_by_key(key):
    _redis.delete(key)
