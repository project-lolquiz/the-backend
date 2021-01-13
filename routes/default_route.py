from flask import Blueprint

default_rest = Blueprint('default_rest', __name__)


@default_rest.route('/')
@default_rest.route('/health')
@default_rest.route('/ping')
def ping():
    return "pong", 200
