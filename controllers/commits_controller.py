from flask import request, Request, jsonify

from db import db
from models.commits import Commits, commit_schema, commits_schema
from models.repositories import Repositories
from util.reflection import populate_obj


def add_commit(req: Request):
    post_data = request.form if request.form else request.json

    fields = ["repo_id", "comment", "position"]

    req_fields = ["repo_id", "comment", "position"]

    missing_fields = []
    for field in fields:
        field_data = post_data.get(field)
        if field_data in req_fields and not field_data:
            missing_fields.append(field)

        if len(missing_fields):
            return jsonify(f"missing required field(s): {missing_fields}", 400)

    repo_check = db.session.query(Repositories).filter(Repositories.repo_id == post_data["repo_id"]).first()

    if not repo_check:
        return jsonify(f"repo {post_data['repo_id']}not found")

    new_commit = Commits.new_commit()
    populate_obj(new_commit, post_data)

    db.session.add(new_commit)
    db.session.commit()
    commit_data = commit_schema.dump(new_commit)
    commit_data["repo_id"] = repo_check

    return jsonify({"message": "commit created", "commit info": commit_data}), 201


def get_all_commits(req: Request):
    commits = db.session.query(Commits).all()

    if not commits:
        return jsonify('no commits found'), 404
    else:
        return jsonify(commits_schema.dump(commits)), 200


def get_commit(req: Request, id):
    commit = db.session.query(Commits).filter(Commits.commit_id == id).first()

    if not commit:
        return jsonify('commit not found'), 404
    else:
        return jsonify(commit_schema.dump(commit)), 200


def get_commits_by_repo_id(req: Request, id):
    commits = db.session.query(Commits).filter(Commits.repo_id == id).all()

    if not commits:
        return jsonify('commits not found'), 404
    else:
        return jsonify(commits_schema.dump(commits)), 200


def get_commits_by_repo_id(req: Request, id):
    commits = db.session.query(Commits).filter(id in Commits.current_repo).all()

    if not commits:
        return jsonify('commits not found'), 404
    else:
        return jsonify(commits_schema.dump(commits)), 200


def update_commit(req: Request, id):
    post_data = request.json
    if not post_data:
        post_data = request.form

    commit = db.session.query(Commits).filter(Commits.commit_id == id).first()

    if not commit:
        return jsonify('commit not found'), 404

    populate_obj(commit, post_data)
    db.session.commit()

    return jsonify(commit_schema.dump(commit)), 201


def delete_commit(req: Request, id):
    commit = db.session.query(Commits).filter(Commits.commit_id == id).first()

    if commit:
        db.session.delete(commit)
        db.session.commit()
        return jsonify({"message": "commit deleted"}), 200
    else:
        return jsonify({"message": "commit not found"}), 404
