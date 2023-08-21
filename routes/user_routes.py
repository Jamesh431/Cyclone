from flask import request, Blueprint

from controllers import users_controller as controller

users = Blueprint("users", __name__)


@users.route('/user', methods=["POST"])
def add_user():
    return controller.add_user(request)


@users.route('/users', methods=['GET'])
def get_all_users():
    return controller.get_users(request)


@users.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return controller.get_user_by_id(request, user_id)


@users.route('/user/<user_id>', methods=["PATCH"])
def update_user(user_id):
    return controller.update_user(request, user_id)


@users.route('/user/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    return controller.delete_user(request, user_id)


@users.route('/user/<user_id>', methods=["PATCH"])
def user_activity(user_id):
    return controller.user_activity(request, user_id)
