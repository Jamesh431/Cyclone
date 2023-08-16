# use response 202 for successful session creation if start time is not now ?
from flask import request, Request, jsonify

from db import db
from models.sessions import Sessions, session_schema, sessions_schema
from models.users import Users, user_schema
from util.reflection import populate_obj


def add_session(req: Request):
    req_data = request.form if request.form else request.json

    fields = ["current_repo", "repositories", "num_of_commits", "commit_by_repo_ammount", "time_to_commit", "time_frame", "latest_commit", "current_position", "active"]

    req_fields = ["current_repo", "repositories", "num_of_commits", "commit_by_repo_ammount", "time_frame", "current_position", "active"]

    missing_fields = []

    for field in fields:
        field_data = req_data.get(field)
        if field in req_fields and not field_data:
            missing_fields.append(field)

        if len(missing_fields):
            return jsonify(f"{missing_fields} are required", 400)

    new_session = Sessions.new_session()

    populate_obj(new_session, req_data)

    db.session.add(new_session)
    db.session.commit()

    return jsonify({"message": "session created", "session info": session_schema.dump(new_session)}), 201


def get_all_sessions(req: Request):
    session = db.session.query(Sessions).all()

    if not Sessions:
        return jsonify('No Sessions found'), 404
    else:
        return jsonify(sessions_schema.dump(session)), 200


def get_session(req: Request, id):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify('Session not found'), 404
    else:
        return jsonify(session_schema.dump(session)), 200


def get_sessions_by_user_id(req: Request, user_id, only_active):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    sessions = user_schema.dump(user).get("session", [])

    if not sessions:
        return jsonify('Sessions not found'), 404
    else:
        if not only_active:
            users_sessions = sessions
        else:
            users_sessions = [user_session for user_session in sessions if user_session.get("active", True)]

            grouped_sessions = []
            # include loop here that will loop through user sessions ids, gather all data for each of those sessions then return them below
            for session_id in users_sessions:
                session_query = db.session.query(Sessions).filter(Sessions.session_id == session_id).first()
                session_iteration = session_schema.dump(session_query).first()
                grouped_sessions.append(session_iteration)

    return jsonify(message="sessions found", sessions=grouped_sessions), 200


def get_sessions_by_current_repo_id(req: Request, id):
    sessions = db.session.query(Sessions).filter(Sessions.current_repo == id).all()

    if not sessions:
        return jsonify('Sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


def get_sessions_by_repo_id(req: Request, id):
    sessions = db.session.query(Sessions).filter(id in Sessions.current_repo).all()

    if not sessions:
        return jsonify('Sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


def update_session(req: Request, id):
    post_data = request.json
    if not post_data:
        post_data = request.form

    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify('Session not found'), 404
    else:
        populate_obj(session, post_data)
        db.session.commit()
        return jsonify(session_schema.dump(session)), 201


def delete_session(req: Request, id):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if session:
        db.session.delete(session)
        db.session.commit()
        return jsonify({"message": "Session Deleted"}), 200
    else:
        return jsonify({"message": "Session not found"}), 404
