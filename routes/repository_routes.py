from flask import request, Response, Blueprint

from controllers import repository_controller as controller

repositories = Blueprint("repositories", __name__)


@repositories.route('/repository', methods=["POST"])
def add_repo() -> Response:
    return controller.add_repository(request)
