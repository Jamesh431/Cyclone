from flask import request, Request, jsonify
from flask_bcrypt import generate_password_hash
from github import Github

from db import db
from models.auth_tokens import Auths, auth_schema, auths_schema
from models.users import Users
from util.reflection import populate_obj
from lib.authenticate import *


def add_auth(req: Request):
    post_data = request.form if request.form else request.json

    fields = ['github_token', 'github_username', 'cyclone_pass']
    req_fields = ['github_token', 'github_username', 'cyclone_pass']
    missing_fields = []

    if "cyclone_pass" in post_data:
        post_data["cyclone_pass"] = generate_password_hash(post_data["cyclone_pass"]).decode("utf8")

    for field in fields:
        field_data = post_data.get(field)
        if field in req_fields and not field_data:
            if field == "github_token":
                check_token = db.session.query(Auths).filter(Auths.github_username == post_data["github_username"]).first()
                if check_token:
                    continue
            missing_fields.append(field)

    hashed_pass = post_data.pop("cyclone_pass")

    if len(missing_fields):
        return jsonify(f"missing required field(s): {missing_fields}", 400)

    user_check = db.session.query(Users).filter(Users.github_username == post_data["github_username"] and Users.cyclone_pass == hashed_pass).first()

    if not user_check:
        return jsonify({"message": "invalid login"}), 403

    auth_check = db.session.query(Auths).filter(Auths.github_username == post_data["github_username"]).first()

    if not auth_check:
        new_auth = Auths.new_auth()

        populate_obj(new_auth, post_data)

        auth_check = new_auth

        db.session.add(new_auth)
        db.session.commit()

    auth_data = auth_schema.dump(auth_check)

    try:
        Github(auth_data["github_token"]).get_user(auth_data["github_username"])
    except:
        return jsonify({"message": "invalid github token"}), 401

    return jsonify({"message": "authorized", "auth": auth_data}), 201


@auth_with_return
def get_all_my_auths(req: Request, auth_info):
    auths = db.session.query(Auths).filter(Auths.github_username == auth_info.github_username).all()

    if not auths:
        return jsonify('No Auths found'), 404
    else:
        return jsonify(auths_schema.dump(auths)), 200


@auth
def get_auth(req: Request, id, auth_info):
    auth = db.session.query(Auths).filter(Auths.github_token == id).first()

    if not auth:
        return jsonify('Auth not found'), 404
    else:
        return jsonify(auth_schema.dump(auth)), 200


@auth
def get_auth_by_github_username(req: Request, id, auth_info):
    auth = db.session.query(Auths).filter(Auths.github_username == id).first()

    if not auth:
        return jsonify('Auth not found'), 404
    else:
        return jsonify(auth_schema.dump(auth)), 200


@auth
def update_auth(req: Request, id, auth_info):
    post_data = request.json
    if not post_data:
        post_data = request.form

    auth = db.session.query(Auths).filter(Auths.github_token == id).first()

    if not auth:
        return jsonify('Auth not found'), 404
    else:
        populate_obj(auth, post_data)
        db.session.commit()
        return jsonify(auth_schema.dump(auth)), 201


@auth
def delete_auth(req: Request, id, auth_info):
    auth = db.session.query(Auths).filter(Auths.github_token == id).first()

    if auth:
        db.session.delete(auth)
        db.session.commit()
        return jsonify({"message": "Auth Deleted"}), 200
    else:
        return jsonify({"message": "Auth not found"}), 404


@auth
def auth_activity(req: Request, id, auth_info):
    auth = db.session.query(Auths).filter(Auths.github_token == id).first()

    if not auth:
        return jsonify({"message": "auth not found"}), 404

    auth.active = not auth.active

    db.session.commit()

    return jsonify({"message": "auth updated", "auth": auth_schema.dump(user)}), 200
