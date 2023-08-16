from flask import request, Response, Blueprint

from controllers import sessions_controller as controller

sessions = Blueprint("sessions", __name__)


@sessions.route('/sessions', methods=["POST"])
def add_session() -> Response:
    return controller.add_session(request)


@sessions.route('/sessions/<user_id>/<only_active>', methods=["GET"])
def get_sessions_by_user_id(user_id, only_active) -> Response:
    return controller.get_sessions_by_user_id(request, user_id, only_active)
