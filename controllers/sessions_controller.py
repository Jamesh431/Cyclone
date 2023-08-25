from flask import request, Request, jsonify

from db import db
from models.sessions import Sessions, session_schema, sessions_schema
from models.repositories import Repositories, repos_schema
from models.session_repo_xref import SessionRepoXref
from util.reflection import populate_obj


@auth
def add_session(req: Request, auth_info):
    post_data = request.form if request.form else request.json

    fields = ['session_id', 'receiving_user', 'name', 'current_repo_id', 'num_of_commits', 'commit_by_repo_amount', 'start_time', 'end_time', 'latest_commit', 'current_position', 'active', 'assigned_repos']

    req_fields = ["current_repo_id", "num_of_commits", "commit_by_repo_amount", "start_time", "end_time", "current_position", "active"]

    assigned_repos = None
    repo = None
    if "repositories" in post_data:
        assigned_repos = post_data.pop("repositories")

        for repository_id in assigned_repos:
            repo = db.session.query(Repositories).filter(Repositories.repo_id == repository_id).first()

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
    populate_obj(new_session, post_data)

    db.session.add(new_session)
    # if receiver_id:
    # user_object = db.session.get(Users, receiver_id)
    # print(user)
    # dumped_user = user_schema.dump(user)
    # print(dumped_user["github_username"])
    # new_session.users.append(dumped_user["github_username"]
    db.session.commit()
    session_data = session_schema.dump(new_session)

    if repo:
        for repository in assigned_repos:
            xref_check = db.session.query(SessionRepoXref).filter(SessionRepoXref.session_id == session_data["session_id"]).filter(SessionRepoXref.repo_id == repository).first()

            if xref_check:
                continue

            new_session_repo_relationship = SessionRepoXref.new_session_repo_xref()
            session_repo_dictionary = {'session_id': session_data["session_id"], 'repo_id': repository}
            populate_obj(new_session_repo_relationship, session_repo_dictionary)

            db.session.add(new_session_repo_relationship)
            db.session.commit()

        linked_repos = db.session.query(Repositories).filter(Repositories.repo_id.in_(assigned_repos)).all()

        session_data["repositories"] = repos_schema.dump(linked_repos)

    return jsonify({"message": "session created", "session": session_data}), 201


@auth
def get_all_sessions(req: Request, auth_info):
    sessions = db.session.query(Sessions).all()

    if not sessions:
        return jsonify('no sessions found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


@auth
def get_session(req: Request, id, auth_info):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify('session not found'), 404
    else:
        return jsonify(session_schema.dump(session)), 200


@auth
def get_sessions_by_github_username(req: Request, github_username, show_all, auth_info):
    sessions = None

    if show_all == "all":
        sessions = db.session.query(Sessions).filter(Sessions.receiving_user == github_username).all()
    else:
        sessions = db.session.query(Sessions).filter(Sessions.receiving_user == github_username).filter(Sessions.active == True).all()

    if not sessions:
        return jsonify('sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


@auth
def get_sessions_by_current_repo_id(req: Request, id, auth_info):
    sessions = db.session.query(Sessions).filter(Sessions.current_repo_id == id).all()

    if not sessions:
        return jsonify('sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(sessions)), 200


@auth
def get_sessions_by_repo_id(req: Request, id, auth_info):

    join_sessions_query = db.session.query(Sessions).join(SessionRepoXref, Sessions.session_id == SessionRepoXref.session_id).filter(SessionRepoXref.repo_id == id).all()

    if not join_sessions_query:
        return jsonify('sessions not found'), 404
    else:
        return jsonify(sessions_schema.dump(join_sessions_query)), 200


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


@auth
def update_session(req: Request, id, auth_info):
    post_data = request.json
    if not post_data:
        post_data = request.form

    repo = None
    assigned_repos = []
    repos_to_expunge = []

    if "add_repositories" in post_data:
        assigned_repos = post_data.pop("add_repositories")

        for repository_id in assigned_repos:
            repo = db.session.query(Repositories).filter(Repositories.repo_id == repository_id).first()

            if not repo:
                return jsonify(f"Repo not found: {repository_id}", 404)

    if "delete_repositories" in post_data:
        repos_to_expunge = post_data.pop("delete_repositories")

        for repository_id in repos_to_expunge:
            repo = db.session.query(Repositories).filter(Repositories.repo_id == repository_id).first()

            if not repo:
                return jsonify(f"Repo not found: {repository_id}", 404)

    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify('session not found'), 404

    session_data = session_schema.dump(session)

    if repo:
        if assigned_repos:
            for repository in assigned_repos:
                xref_check = db.session.query(SessionRepoXref).filter(SessionRepoXref.session_id == session_data["session_id"]).filter(SessionRepoXref.repo_id == repository).first()

                if xref_check:
                    continue

                new_session_repo_relationship = SessionRepoXref.new_session_repo_xref()
                session_repo_dictionary = {'session_id': session_data["session_id"], 'repo_id': repository}
                populate_obj(new_session_repo_relationship, session_repo_dictionary)

                db.session.add(new_session_repo_relationship)

        if repos_to_expunge:
            for repository in repos_to_expunge:
                xref_check = db.session.query(SessionRepoXref).filter(SessionRepoXref.session_id == session_data["session_id"]).filter(SessionRepoXref.repo_id == repository).first()

                if xref_check:
                    db.session.delete(xref_check)

        db.session.commit()

        linked_repos = db.session.query(Repositories).filter(Repositories.repo_id.in_(assigned_repos)).all()

        session_data["repositories"] = repos_schema.dump(linked_repos)

    populate_obj(session, post_data)
    db.session.commit()
    return jsonify({"message": "session updated", "session": session_data}), 201


@auth
def delete_session(req: Request, id, auth_info):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if session:
        check_xref = db.session.query(SessionRepoXref).filter(SessionRepoXref.session_id == id).all()

        if check_xref:
            for relationship in check_xref:
                db.session.delete(relationship)
            db.session.commit()

        db.session.delete(session)
        db.session.commit()
        return jsonify({"message": "session deleted"}), 200
    else:
        return jsonify({"message": "session not found"}), 404


@auth
def session_activity(req: Request, id, auth_info):
    session = db.session.query(Sessions).filter(Sessions.session_id == id).first()

    if not session:
        return jsonify({"message": "session not found"}), 404

    session.active = not session.active

    db.session.commit()

    return jsonify({"message": "session updated", "session": session_schema.dump(session)}), 200
