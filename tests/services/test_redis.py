import os

os.environ['ENV'] = 'qa'

import json

from services.redis_service import add, get_by_key, get_all, delete_by_key, delete_all, set_content


def test_set_content_and_get():
    key = 'the-key'
    json_body = {'value': 'the-value'}

    set_content(key, json_body, 60)
    redis_content = get_by_key(key)

    json_dict = json.loads(redis_content)
    assert json_dict
    assert 'value' in json_dict
    assert json_dict['value'] == json_body['value']


def test_add_and_get():
    json_body = {'key': 'the-key', 'value': 'the-value', 'expires_in': 10}
    add(json_body)

    redis_content = get_by_key(json_body['key'])
    json_dict = json.loads(redis_content)  # Convert from string to dict
    assert json_dict
    assert 'key' in json_dict
    assert json_dict['key'] == json_body['key']
    assert 'value' in redis_content
    assert json_dict['value'] == json_body['value']
    assert 'expires_in' in redis_content
    assert json_dict['expires_in'] == json_body['expires_in']


def test_add_without_expires_in_and_get():
    json_body = {'key': 'the-key', 'value': 'the-value', 'expires_in': None}
    add(json_body)

    redis_content = get_by_key(json_body['key'])
    json_dict = json.loads(redis_content)  # Convert from string to dict
    assert json_dict
    assert 'key' in json_dict
    assert json_dict['key'] == json_body['key']
    assert 'value' in redis_content
    assert json_dict['value'] == json_body['value']
    assert 'expires_in' in redis_content
    assert json_dict['expires_in'] is None


def test_get_all():
    redis_content = get_all()
    assert redis_content
    assert len(redis_content) > 0


def test_delete_by_key():
    key = 'version'
    assert get_by_key(key)

    delete_by_key(key)
    assert not get_by_key(key)


def test_delete_all():
    redis_current_keys = get_all().keys()
    assert len(redis_current_keys) > 0

    delete_all()
    for key in redis_current_keys:
        assert not get_by_key(key)