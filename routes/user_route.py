from flask import jsonify, Blueprint, request

from services.user_service import *

user_rest = Blueprint('user_rest', __name__)


@user_rest.route('/users/register', methods=['post'])
def user_register():
    return add_user(request.get_json()), 201


@user_rest.route('/users/<string:uid>', methods=['put'])
def user_update(uid):
    update_user(uid, request.get_json())
    return '', 204


@user_rest.route('/users/<string:uid>/avatar', methods=['put'])
def user_avatar_update(uid):
    update_avatar(uid, request.get_json())
    return '', 204


@user_rest.route('/users/<string:uid>')
def user_get(uid):
    current_user = get_user_by_uid(uid)
    if current_user:
        return jsonify(current_user), 200
    else:
        return jsonify({'error': 'User {} not found'.format(uid)}), 404
