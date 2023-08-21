from flask import request, Response, Blueprint

from controllers import sessions_controller as controller

sessions = Blueprint("sessions", __name__)


@sessions.route('/session', methods=["POST"])
def add_session() -> Response:
    return controller.add_session(request)


@sessions.route('/sessions', methods=["GET"])
def get_all_sessions() -> Response:
    return controller.get_all_sessions(request)


@sessions.route('/sessions/u/<user_id>/<show_all>', methods=["GET"])
def get_sessions_by_user_id(user_id, show_all) -> Response:
    return controller.get_sessions_by_user_id(request, user_id, show_all)


@sessions.route('/sessions/current_repo/<repo_id>', methods=["GET"])
def get_sessions_by_current_repo(repo_id) -> Response:
    return controller.get_sessions_by_current_repo_id(request, repo_id)


@sessions.route('/sessions/repo/<repo_id>', methods=["GET"])
def get_sessions_by_repo(repo_id) -> Response:
    return controller.get_sessions_by_repo_id(request, repo_id)


@sessions.route('/session/<id>', methods=["PATCH"])
def update_session(session_id) -> Response:
    return controller.update_session(request, session_id)


@sessions.route('/session/<id>', methods=["DELETE"])
def delete_session(session_id) -> Response:
    return controller.delete_session(request, session_id)


@session.route('/session/status/<id>', methods=["PATCH"])
def session_activity(session_id) -> Response:
    return controller.session_activity(request, session_id)
