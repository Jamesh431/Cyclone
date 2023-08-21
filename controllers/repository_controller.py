from flask import request, Request, jsonify

from db import db
from models.repositories import Repositories, repo_schema, repos_schema
from util.reflection import populate_obj


def add_repository(req: Request):
    req_data = request.form if request.form else request.json
    fields = ["sender_id", "name", "branches", "active"]
    req_fields = ["sender_id", "name", "active"]
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

    return jsonify({"message": "repository created", "repository_info": repo_schema.dump(new_repository)}), 201
