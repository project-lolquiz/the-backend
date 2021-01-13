from flask import jsonify, Blueprint, request

from services.user_service import *

user_rest = Blueprint('user_rest', __name__)


@user_rest.route('/users/register', methods=['post'])
def user_register():
    try:
        return jsonify(add_user(request.get_json())), 201
    except UserAlreadyExists as uae:
        return json_error_message(uae.message), 400


@user_rest.route('/users/<string:uid>', methods=['put'])
def user_update(uid):
    try:
        update_user(uid, request.get_json())
    except UserNotFound as unf:
        return json_error_message(unf.message), 404
    return '', 204


@user_rest.route('/users/<string:uid>/avatar', methods=['put'])
def user_avatar_update(uid):
    try:
        update_avatar(uid, request.get_json())
    except UserNotFound as unf:
        return json_error_message(unf.message), 404
    return '', 204


@user_rest.route('/users/<string:uid>')
def user_get(uid):
    current_user = get_user_by_uid(uid)
    if current_user:
        return jsonify(current_user), 200
    else:
        return json_error_message('User {} not found'.format(uid)), 404


def json_error_message(message):
    return jsonify({'error': message})
