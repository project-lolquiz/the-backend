from flask import jsonify, Blueprint

from services.redis_client import get_all as from_redis
from services.simple_service import get_all as from_db


dumb_rest = Blueprint('dumb_rest', __name__)


@dumb_rest.route('/redis-get-all')
def redis_get_all():
    return jsonify(from_redis()), 200


@dumb_rest.route('/db-get-all')
def db_get_all():
    return jsonify(from_db())
