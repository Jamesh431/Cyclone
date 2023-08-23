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
def get_user_by_id(github_username):
    return controller.get_user_by_github_username(request, github_username)


@users.route('/user/<github_username>', methods=["PATCH"])
def update_user(github_username):
    return controller.update_user(request, github_username)


@users.route('/user/status/<github_username>', methods=["PATCH"])
def user_activity(github_username):
    return controller.user_activity(request, github_username)


@users.route('/user/<github_username>', methods=["DELETE"])
def delete_user(github_username):
    return controller.delete_user(request, github_username)
