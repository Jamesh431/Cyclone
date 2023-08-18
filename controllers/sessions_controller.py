# use response 202 for successful session creation if start time is not now ?
from flask import request, Request, jsonify
from sqlalchemy.orm import aliased

from db import db
from models.sessions import Sessions, session_schema, sessions_schema
from models.repositories import Repositories, repos_schema
from models.user_sessions_xref import user_sessions_xref
from util.reflection import populate_obj


def add_session(req: Request):
    post_data = request.form if request.form else request.json

    fields = ["current_repo_id", "repositories", "num_of_commits", "commit_by_repo_amount", "time_to_commit", "time_frame", "latest_commit", "current_position", "active"]

    req_fields = ["current_repo_id", "repositories", "num_of_commits", "commit_by_repo_amount", "time_frame", "current_position", "active"]
    assigned_repos = None
    repo = None
    if "assigned_repos" in post_data:
        assigned_repos = post_data.get("assigned_repos")
        repo = db.session.query(Repositories).filter(Repositories.repo_id == assigned_repos).first()

        if not repo:
            return jsonify(f"Repo not found: {assigned_repos}", 404)

    missing_fields = []
    for field in fields:
        field_data = post_data.get(field)
        if field_data in req_fields and not field_data:
            missing_fields.append(field)

        if len(missing_fields):
            return jsonify(f"{missing_fields} are required", 400)

    new_session = Sessions.create_session()
    print(new_session)
    populate_obj(new_session, post_data)

    db.session.add(new_session)
    # if receiver_id:
    # user_object = db.session.get(Users, receiver_id)
    # print(user)
    # dumped_user = user_schema.dump(user)
    # print(dumped_user["user_id"])
    # new_session.users.append(dumped_user["user_id"])
    db.session.commit()

    # return jsonify(session_schema.dump(new_session))

    session_data = session_schema.dump(new_session)
    print(session_data)

    if repo:
        fetched_session = db.session.query(Sessions).filter(Sessions.session_id == session_data['session_id']).first()

        print(fetched_session)

        fetched_session.assigned_repos.append(repo)

        session_data = fetched_session

    return jsonify({"message": "session created", "session info": session_data}), 201


def get_all_sessions(req: Request):
    sessions = db.session.query(Sessions).all()

    if not sessions:
        return jsonify('No Sessions found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


def get_session(req: Request, id):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify('Session not found'), 404
    else:
        return jsonify(session_schema.dump(session)), 200


# def tasks_get_by_user_id(req: Request, user_id, auth_info) -> Response:
#     if validate_uuid4(user_id) == False:
#         Logger("Invalid User ID, 400", "Bad Request")
#         return jsonify({"message": "invalid id"}), 400

#     user = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
#     xref_alias = aliased(user_sessions_xref)
#     db.session.query(Sessions).join(xref_alias, Sessions.session_id == xref_alias.c.session_id).filter(xref_alias.c.user_id == user)
#     user_tasks =.filter(Tasks.assigned_users.any(AppUsers.user_id == user_id)).all()

#     if not auth_info.user.role == "super-admin" and not auth_info.user.role == "admin":
#         user_tasks = [task for task in user_tasks if task.active == True]

#     return jsonify({"message": "tasks found", "tasks": tasks_schema.dump(user_tasks)}), 200


def get_sessions_by_user_id(req: Request, user_id, show_all):

    # xref_alias = aliased(user_sessions_xref)

    # all_users_sessions = db.session.query(Sessions).join(xref_alias, Sessions.session_id == xref_alias.c.session_id).filter(xref_alias.c.receiver_id == user_id).all()
    all_users_sessions = db.session.query(Sessions).join(user_sessions_xref).filter(user_sessions_xref.columns.receiver_id == user_id).all()
    users_sessions = all_users_sessions
    # sessions = sessions_schema.dump(query)

    # user = db.session.query(Users).filter(Users.user_id == user_id).first()
    # sessions = user_schema.dump(user).get("session", [])

    if not all_users_sessions:
        return jsonify('Sessions not found'), 404
    else:
        if not show_all:
            users_sessions = [user_session for user_session in all_users_sessions if user_session.get("active", True)]

    return jsonify({"message": "sessions found", "all_sessions": sessions_schema.dump(users_sessions)}), 200

    #         grouped_sessions = []
    #         # include loop here that will loop through user sessions ids, gather all data for each of those sessions then return them below
    #         for session_id in users_sessions:
    #             session_query = db.session.query(Sessions).filter(Sessions.session_id == session_id).first()
    #             session_iteration = session_schema.dump(session_query).first()
    #             grouped_sessions.append(session_iteration)

    # return jsonify(message="sessions found", sessions=grouped_sessions), 200


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
