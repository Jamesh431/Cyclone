from flask import request, Blueprint

from controllers import auth_tokens_controller as controller

auths = Blueprint('Auth', __name__)


@auths.route('/auth', methods=["POST"])
def add_authorization():
    return controller.add_auth(request)


@auths.route("/auths", methods=["GET"])
def get_all_auths():
    return controller.get_all_auths(request)


@auths.route("/auth/<id>", methods=["GET"])
def get_auth_by_id(id):
    return controller.get_auth(request, id)


@auths.route('/auth/u/<user_id>', methods=['GET'])
def get_auth_by_user_id(user_id):
    return controller.get_auth_by_user_id(request, user_id)


@auths.route('/auth/<auth_id>', methods=["PATCH"])
def update_auth(auth_id):
    return controller.update_auth(request, auth_id)


@auths.route('/auth/status/<github_token>', methods=["PATCH"])
def auth_activity(github_token):
    return controller.auth_activity(request, github_token)


@auths.route('/auth/<auth_id>', methods=["DELETE"])
def delete_auth(auth_id):
    return controller.delete_auth(request, auth_id)
