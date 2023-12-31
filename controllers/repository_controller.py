from flask import request, Request, jsonify

from db import db
from models.repositories import Repositories, repo_schema, repos_schema
from util.reflection import populate_obj
from lib.authenticate import *


@auth
def add_repository(req: Request, auth_info):
    req_data = request.form if request.form else request.json
    fields = ["senders_github_username", "name", "ssh_key", "branches", "active"]
    req_fields = ["senders_github_username", "name", "ssh_key", "active"]
    missing_fields = []

    for field in fields:
        field_data = req_data.get(field)
        if field in req_fields and not field_data:
            missing_fields.append(field)

    if len(missing_fields):
        return jsonify(f"missing required field(s): {missing_fields}", 400)

    new_repository = Repositories.new_repository()

    populate_obj(new_repository, req_data)

    db.session.add(new_repository)
    db.session.commit()

    return jsonify({"message": "repository created", "repository": repo_schema.dump(new_repository)}), 201


@auth
def get_all_repositories(req: Request, auth_info):
    all_repositories = db.session.query(Repositories).all()

    if all_repositories:
        return jsonify({"message": "repositories found", "repositories": repos_schema.dump(all_repositories)}), 200
    else:
        return jsonify({"message": "repositories not found"}), 404


@auth
def get_active_repositories(req: Request, auth_info):
    active_repositories = db.session.query(Repositories).filter(Repositories.active == True).all()

    if active_repositories:
        return jsonify({"message": "repositories found", "repositories": repos_schema.dump(active_repositories)}), 200
    else:
        return jsonify({"message": "repositories not found"}), 404


@auth
def get_repository(req: Request, id, auth_info):
    repository = db.session.query(Repositories).filter(Repositories.repo_id == id).first()

    if repository:
        return jsonify({"message": "repository found", "repository": repo_schema.dump(repository)}), 200
    else:
        return jsonify({"message": "repository not found"}), 404


@auth
def get_repository_by_search(req: Request, auth_info):
    formatted_search = req.args.get('q').lower()

    search_query = db.session.query(Repositories).filter(db.or_(db.func.lower(Repositories.name).contains(formatted_search)))

    search_data = search_query.order_by(Repositories.name.asc()).all()

    return jsonify({"message": "results", "repositories": repos_schema.dump(search_data)}), 200


@auth
def get_repositories_by_senders_github_username(req: Request, id, auth_info):
    senders_repositories = db.session.query(Repositories).filter(Repositories.senders_github_username == id).all()

    if senders_repositories:
        return jsonify({"message": "repositories found", "repositories": repos_schema.dump(senders_repositories)}), 200
    else:
        return jsonify({"message": "repositories not found"}), 404


@auth
def update_repository(req: Request, id, auth_info):
    patch_data = request.json
    if not patch_data:
        patch_data = request.form

    repository_data = db.session.query(Repositories).filter(Repositories.repo_id == id).first()

    if not repository_data:
        return jsonify({"message": "repository not found"}), 404

    populate_obj(repository_data, patch_data)
    db.session.commit()

    return jsonify({"message": "repostory updated", "repository": repo_schema.dump(repository_data)}), 200


@auth
def delete_repository(req: Request, id, auth_info):
    expunged_repository = db.session.query(Repositories).filter(Repositories.repo_id == id).first()

    if not expunged_repository:
        return jsonify({"message": "repository not found"}), 404

    db.session.delete(expunged_repository)
    db.session.commit()

    return jsonify({"message": "repository deleted"}), 200


@auth
def repository_activity(req: Request, id, auth_info):
    repository = db.session.query(Repositories).filter(Repositories.repo_id == id).first()

    if not repository:
        return jsonify({"message": "repository not found"}), 404

    repository.active = not repository.active

    db.session.commit()

    return jsonify({"message": "repository updated", "repository": repo_schema.dump(repository)}), 200
