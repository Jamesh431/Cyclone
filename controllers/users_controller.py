from flask import request, Request, jsonify

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_obj


def add_user(req: Request):
    req_data = request.form if request.form else request.json
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

    return jsonify({"message": "user created", "user": user_schema.dump(new_user)}), 201


def get_users(req: Request):
    users = db.session.query(Users).all()

    return jsonify(users_schema.dump(users)), 200


def get_user_by_id(req: Request, user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if user:
        return jsonify(user_schema.dump(user)), 200

    return jsonify("User Not Found"), 404
