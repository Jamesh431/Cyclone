from flask import request, Response, Blueprint

from controllers import users_controller as controller

users = Blueprint("users", __name__)


@users.route('/user', methods=["POST"])
def add_user() -> Response:
    return controller.add_user(request)


@users.route('/users', methods=['GET'])
def get_all_users() -> Response:
    return controller.get_users(request)


@users.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id) -> Response:
    return controller.get_user_by_id(request, user_id)
