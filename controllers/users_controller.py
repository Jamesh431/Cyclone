from flask import request, Request, jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_obj


def add_user(req: Request):
    post_data = request.form if request.form else request.json
    fields = ["github_username", "cyclone_pass", "active"]
    req_fields = ["github_username", "cyclone_pass", "active"]

    if "cyclone_pass" in post_data:
        print(post_data["cyclone_pass"])
        post_data["cyclone_pass"] = generate_password_hash(post_data["cyclone_pass"]).decode("utf8")

    missing_fields = []

    for field in fields:
        field_data = post_data.get(field)
        if field in req_fields and not field_data:
            missing_fields.append(field)

    if len(missing_fields):
        return jsonify(f"missing required field(s): {missing_fields}", 400)

    new_user = Users.new_user()

    populate_obj(new_user, post_data)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user created", "user": user_schema.dump(new_user)}), 201


def get_users(req: Request):
    users = db.session.query(Users).all()

    return jsonify(users_schema.dump(users)), 200


def get_user_by_github_username(req: Request, github_username):
    user = db.session.query(Users).filter(Users.github_username == github_username).first()
    if user:
        return jsonify(user_schema.dump(user)), 200

    return jsonify("User Not Found"), 404


def update_user(req: Request, github_username):
    patch_data = request.json
    if not patch_data:
        patch_data = request.form

    if "cyclone_pass" in patch_data:
        patch_data["cyclone_pass"] = generate_password_hash(patch_data["cyclone_pass"]).decode("utf8")

    user = db.session.query(Users).filter(Users.github_username == github_username).first()

    if not user:
        return jsonify('User not found'), 404

    populate_obj(user, patch_data)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201


def delete_user(req: Request, github_username):
    user = db.session.query(Users).filter(Users.github_username == github_username).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "user deleted"}), 200
    else:
        return jsonify({"message": "user not found"}), 404


def user_activity(req: Request, github_username):
    user = db.session.query(Users).filter(Users.github_username == github_username).first()

    if not user:
        return jsonify({"message": "user not found"}), 404

    user.active = not user.active

    db.session.commit()

    return jsonify({"message": "user updated", "user": user_schema.dump(user)}), 200
