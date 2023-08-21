# use response 202 for successful session creation if start time is not now ?
from flask import request, Request, jsonify
# from sqlalchemy.orm import aliased

from db import db
from models.sessions import Sessions, session_schema, sessions_schema
from models.repositories import Repositories, repos_schema
from models.session_repo_xref import SessionRepoXref, session_repo_xrefs
from util.reflection import populate_obj


def add_session(req: Request):
    post_data = request.form if request.form else request.json

    fields = ['session_id', 'receiving_user', 'name', 'current_repo_id', 'num_of_commits', 'commit_by_repo_amount', 'start_time', 'end_time', 'latest_commit', 'current_position', 'active', 'assigned_repos']

    req_fields = ["current_repo_id", "num_of_commits", "commit_by_repo_amount", "start_time", "end_time", "current_position", "active"]

    assigned_repos = None
    repo = None
    if "repositories" in post_data:
        assigned_repos = post_data.pop("repositories")

        for repository_id in assigned_repos:
            repo = db.session.query(Repositories).filter(Repositories.repo_id == repository_id).first()
            # print("\n")
            # print(repos_schema.dump(repo))  # can be used to grab each repo ["repo_id"]
            # print("\n")

        if not repo:
            return jsonify(f"Repo not found: {assigned_repos}", 404)

    missing_fields = []
    for field in fields:
        field_data = post_data.get(field)
        if field_data in req_fields and not field_data:
            missing_fields.append(field)

        if len(missing_fields):
            return jsonify(f"{missing_fields} are required", 400)

    new_session = Sessions.new_session()
    # print(new_session.session_id)
    populate_obj(new_session, post_data)

    db.session.add(new_session)
    # if receiver_id:
    # user_object = db.session.get(Users, receiver_id)
    # print(user)
    # dumped_user = user_schema.dump(user)
    # print(dumped_user["user_id"])
    # new_session.users.append(dumped_user["user_id"]
    db.session.commit()
    session_data = session_schema.dump(new_session)

    if repo:
        for repository in assigned_repos:
            xref_check = db.session.query(SessionRepoXref).filter(SessionRepoXref.session_id == session_data["session_id"]).filter(SessionRepoXref.repo_id == repository).first()

            if xref_check:
                print('xref relationship already exists')
                continue

            new_session_repo_relationship = SessionRepoXref.new_session_repo_xref()
            session_repo_dictionary = {'session_id': session_data["session_id"], 'repo_id': repository}
            populate_obj(new_session_repo_relationship, session_repo_dictionary)

            db.session.add(new_session_repo_relationship)
            db.session.commit()

        linked_repos = db.session.query(Repositories).filter(Repositories.repo_id.in_(assigned_repos)).all()

        session_data["repositories"] = repos_schema.dump(linked_repos)

    return jsonify({"message": "session created", "session info": session_data}), 201


def get_all_sessions(req: Request):
    sessions = db.session.query(Sessions).all()

    if not sessions:
        return jsonify('no sessions found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


def get_session(req: Request, id):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify('session not found'), 404
    else:
        return jsonify(session_schema.dump(session)), 200


def get_sessions_by_user_id(req: Request, user_id, show_all):
    sessions = db.session.query(Sessions).filter(Sessions.receiving_user == user_id).all()

    if not sessions:
        return jsonify('sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


def get_sessions_by_current_repo_id(req: Request, id):
    sessions = db.session.query(Sessions).filter(Sessions.current_repo == id).all()

    if not sessions:
        return jsonify('sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


def get_sessions_by_repo_id(req: Request, id):
    sessions = db.session.query(Sessions).filter(id in Sessions.current_repo).all()

    if not sessions:
        return jsonify('sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


# def update_session(req: Request, id):
#     post_data = request.json
#     if not post_data:
#         post_data = request.form

#     session = db.session.query(Sessions).filter(Sessions.session_id == id).first()
#     assigned_repo = post_data.get("assigned_repos")

#     if not session:
#         return jsonify('Session not found'), 404

#     if assigned_repo:
#         repo_query = db.session.query(Repositories).filter(Repositories.repo_id == assigned_repo).first()
#         session.assigned_repos.append(repo_query)

#     populate_obj(session, post_data)
#     db.session.commit()
#     return jsonify(session_schema.dump(session)), 201


def update_session(req: Request, id):
    post_data = request.json
    if not post_data:
        post_data = request.form

    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()
    assigned_repos = post_data.get("repositories")

    if not session:
        return jsonify('session not found'), 404

    if assigned_repos:
        repo_query = db.session.query(Repositories).filter(Repositories.repo_id.in_(assigned_repos)).all()
        print(repo_query)
        session.assigned_repos = session.assigned_repos + repo_query

        for repo in repo_query:
            session.assigned_repos.append(repo)

    populate_obj(session, post_data)
    db.session.commit()
    return jsonify(session_schema.dump(session)), 201


def delete_session(req: Request, id):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if session:
        db.session.delete(session)
        db.session.commit()
        return jsonify({"message": "session deleted"}), 204
    else:
        return jsonify({"message": "session not found"}), 404


def session_activity(req: Request, id):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify({"message": "session not found"}), 404

    session.active = not session.active

    db.session.commit()

    return jsonify({"message": "session updated", "session": session_schema.dump(session)}), 200
