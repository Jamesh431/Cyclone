from flask import request, Blueprint

from controllers import sessions_controller as controller

sessions = Blueprint("sessions", __name__)


@sessions.route('/session', methods=["POST"])
def add_session():
    return controller.add_session(request)


@sessions.route('/session/<session_id>', methods=["GET"])
def get_session(session_id):
    return controller.get_session(request, session_id)


@sessions.route('/sessions', methods=["GET"])
def get_all_sessions():
    return controller.get_all_sessions(request)


@sessions.route('/sessions/u/<user_id>/<show_all>', methods=["GET"])
def get_sessions_by_user_id(user_id, show_all):
    return controller.get_sessions_by_user_id(request, user_id, show_all)


@sessions.route('/sessions/current_repo/<repo_id>', methods=["GET"])
def get_sessions_by_current_repo(repo_id):
    return controller.get_sessions_by_current_repo_id(request, repo_id)


@sessions.route('/sessions/repo/<repo_id>', methods=["GET"])
def get_sessions_by_repo(repo_id):
    return controller.get_sessions_by_repo_id(request, repo_id)


@sessions.route('/session/<session_id>', methods=["PATCH"])
def update_session(session_id):
    return controller.update_session(request, session_id)


@sessions.route('/session/<session_id>', methods=["DELETE"])
def delete_session(session_id):
    return controller.delete_session(request, session_id)


@sessions.route('/session/status/<session_id>', methods=["PATCH"])
def session_activity(session_id):
    return controller.session_activity(request, session_id)
