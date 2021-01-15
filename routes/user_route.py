from flasgger import swag_from
from flask import jsonify, Blueprint, request
from flask_expects_json import expects_json

from services.user_service import *
from routes.default_route import json_error_message
from .schemas.user_schema import *

user_rest = Blueprint('user_rest', __name__)


@user_rest.route('/users/register', methods=['post'])
@expects_json(post_schema)
@swag_from('./docs/user/user_register.yml')
def user_register():
    try:
        return jsonify(add_user(request.get_json())), 201
    except UserAlreadyExists as uae:
        return json_error_message(uae.message), 400


@user_rest.route('/users/<string:uid>', methods=['put'])
@expects_json(put_schema)
@swag_from('./docs/user/user_update.yml')
def user_update(uid):
    try:
        update_user(uid, request.get_json())
    except UserNotFound as unf:
        return json_error_message(unf.message), 404
    return '', 204


@user_rest.route('/users/<string:uid>/avatar', methods=['put'])
@expects_json(put_avatar_schema)
@swag_from('./docs/user/user_avatar_update.yml')
def user_avatar_update(uid):
    try:
        update_avatar(uid, request.get_json())
    except UserNotFound as unf:
        return json_error_message(unf.message), 404
    return '', 204


@user_rest.route('/users/<string:uid>')
@swag_from('./docs/user/user_get.yml')
def user_get(uid):
    current_user = get_user_by_uid(uid)
    if current_user:
        return jsonify(current_user), 200
    else:
        return json_error_message('User {} not found'.format(uid)), 404
