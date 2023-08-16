from flask import request, Request, jsonify

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_obj


def add_user(req: Request):
    req_data = req_data = request.form if request.form else request.json
    fields = ["github_username"]
    req_fields = ["github_username"]

    missing_fields = []

    for field in fields:
        field_data = req_data.get(field)
        if field in req_fields and not field_data:
            missing_fields.append(field)

        if len(missing_fields):
            return jsonify(f"{missing_fields} are required", 400)

    new_user = Users.new_user()

    populate_obj(new_user, req_data)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user created", "user info": user_schema.dump(new_user)}), 201
