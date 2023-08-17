from flask import request, Response, Blueprint

from controllers import sessions_controller as controller

sessions = Blueprint("sessions", __name__)


@sessions.route('/session', methods=["POST"])
def add_session() -> Response:
    return controller.add_session(request)


@sessions.route('/sessions/u/<user_id>/<show_all>', methods=["GET"])
def get_sessions_by_user_id(user_id, show_all) -> Response:
    return controller.get_sessions_by_user_id(request, user_id, show_all)


@sessions.route('/session/<id>', methods=["PATCH"])
def update_session(id) -> Response:
    return controller.update_session(request, id)
