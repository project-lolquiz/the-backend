from datetime import datetime
from flask import jsonify, Blueprint

default_rest = Blueprint('default_rest', __name__)


@default_rest.route('/')
@default_rest.route('/health')
@default_rest.route('/ping')
def ping():
    return "pong", 200


def json_error_message(message):
    return jsonify({'error': message, 'timestamp': str(datetime.now())})