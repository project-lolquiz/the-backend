import json

from flasgger import swag_from
from flask import jsonify, Blueprint, request

from routes.default_route import json_error_message
from services.redis_service import get_all as from_redis, add as into_redis, get_by_key, delete_all, delete_by_key
from services.simple_service import get_all as from_db, add as into_db, get_by_id

dumb_rest = Blueprint('dumb_rest', __name__)


@dumb_rest.route('/redis-add', methods=['post'])
def redis_add():
    into_redis(request.get_json())
    return request.get_json(), 201


@dumb_rest.route('/redis-get-by-key/<string:key>')
@swag_from('./docs/redis/get_redis.yml')
def redis_get_by_key(key):
    try:
        content = get_by_key(key)
        return jsonify({'key': key, 'value': json.loads(content)}), 200
    except Exception as _:
        return json_error_message('Key {} not found'.format(key)), 404


@dumb_rest.route('/redis-get-all')
def redis_get_all():
    return jsonify(from_redis()), 200


@dumb_rest.route('/redis-delete-all', methods=['delete'])
def redis_delete_all():
    delete_all()
    return '', 204


@dumb_rest.route('/redis-delete-by-key/<string:key>', methods=['delete'])
def redis_delete_by_key(key):
    delete_by_key(key)
    return '', 204


@dumb_rest.route('/db-add', methods=['post'])
def db_add():
    into_db(request.get_json())
    return request.get_json(), 201


@dumb_rest.route('/db-get-by-id/<int:by_id>')
def db_get_by_id(by_id):
    simple = get_by_id(by_id)
    print(simple)
    return jsonify(simple), 200


@dumb_rest.route('/db-get-all')
def db_get_all():
    return jsonify(from_db())
