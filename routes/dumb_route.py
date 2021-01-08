from flask import jsonify, Blueprint, request

from services.redis_service import get_all as from_redis, add, get_by_key
from services.simple_service import get_all as from_db

dumb_rest = Blueprint('dumb_rest', __name__)


@dumb_rest.route('/redis-add', methods=['post'])
def redis_add():
    add(request.get_json())
    return request.get_json(), 201


@dumb_rest.route('/redis-get-by-key/<string:key>')
def redis_get_by_key(key):
    content = get_by_key(key)
    return {'key': key, 'value': content}, 200


@dumb_rest.route('/redis-get-all')
def redis_get_all():
    return jsonify(from_redis()), 200


@dumb_rest.route('/db-get-all')
def db_get_all():
    return jsonify(from_db())
