from flask import jsonify, Blueprint

from models.simple import Simple
from services.redis_client import get_all


dumb_rest = Blueprint('dumb_rest', __name__)


@dumb_rest.route('/redis-get-all')
def redis_get_all():
    return jsonify(get_all()), 200


@dumb_rest.route('/db-get-all')
def db_get_all():
    return jsonify([{'id': simple.id, 'value': simple.name} for simple in Simple.query.all()])
