from flask import request, Response, Blueprint

from controllers import users_controller as controller

users = Blueprint("users", __name__)


@users.route('/user', methods=["POST"])
def add_user() -> Response:
    return controller.add_user(request)
