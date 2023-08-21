# from flask import request, Response, Blueprint

# from controllers import exercise_types_controller as controller

# ex_type = Blueprint("ex_type", __name__)


# @ex_type.route('/exercise-type', methods=["POST"])
# def add_ex_type() -> Response:
#     return controller.add_exercise_type(request)


# @ex_type.route('/exercise-types', methods=["GET"])
# def get_all_ex_types() -> Response:
#     return controller.get_all_exercise_types(request)


# @ex_type.route('/exercise-type/<id>', methods=['GET'])
# def get_ex_type(id) -> Response:
#     return controller.get_exercise_type(request, id)


# @ex_type.route('/exercise-type/<id>', methods=['PUT'])
# def update_ex_type(id) -> Response:
#     return controller.update_exercise_type(request, id)


# @ex_type.route('/exercise-type/<id>', methods=['DELETE'])
# def delete_ex_type(id) -> Response:
#     return controller.delete_exercise_type(request, id)


from flask import request, Blueprint

from controllers import auth_tokens_controller as controller

auths = Blueprint('Auth', __name__)


@auths.route('/auth', methods=["POST"])
def add_authorization():
    return controller.add_auth()


@auths.route("/auth", methods=["GET"])
def get_all_auths():
    return controller.get_all_auths()


@auths.route("/auth<id>", methods=["GET"])
def get_auth_by_id(id):
    return controller.get_auth(id)


@auths.route('/auth/<user_id>', methods=['GET'])
def get_auth_by_user_id(user_id):
    return controller.get_auth_by_user_id(request, user_id)


@auths.route('/auth/<auth_id>', methods=["PATCH"])
def update_auth(auth_id):
    return controller.update_auth(request, auth_id)


@auths.route('/auth/<auth_id>', methods=["DELETE"])
def delete_auth(auth_id):
    return controller.delete_auth(request, auth_id)


@auths.route('/auth/<github_token>', methods=["PATCH"])
def auth_activity(github_token):
    return controller.auth_activity(request, github_token)
