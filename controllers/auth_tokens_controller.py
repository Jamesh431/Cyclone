from flask import request, Request, jsonify
import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.auth_tokens import Auths, auth_schema, auths_schema
from util.reflection import populate_obj


def add_auth(req: Request):
    req_data = request.form if request.form else request.json

    fields = ['github_token', 'user_id']
    req_fields = ['github_token', 'user_id']
    missing_fields = []

    for field in fields:
        field_data = req_data.get(field)
        if field in req_fields and not field_data:
            missing_fields.append(field)

        if len(missing_fields):
            return jsonify(f"{missing_fields} are required", 400)

    new_auth = Auths.new_auth()

    populate_obj(new_auth, req_data)

    db.session.add(new_auth)
    db.session.commit()

    return jsonify({"message": "auth created", "auth_info": auth_schema.dump(new_auth)}), 201


def get_all_auths(req: Request):
    auths = db.session.query(Auths).all()

    if not auths:
        return jsonify('No Auths found'), 404
    else:
        return jsonify(auths_schema.dump(auths)), 200


def get_auth(req: Request, id):
    auth = db.session.query(Auths).filter(Auths.github_token == id).first()

    if not auth:
        return jsonify('Auth not found'), 404
    else:
        return jsonify(auth_schema.dump(auth)), 200


def get_auth_by_user_id(req: Request, id):
    auth = db.session.query(Auths).filter(Auths.user_id == id).first()

    if not auth:
        return jsonify('Auth not found'), 404
    else:
        return jsonify(auth_schema.dump(auth)), 200


def update_auth(req: Request, id):
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


def delete_auth(req: Request, id):
    auth = db.session.query(Auths).filter(Auths.github_token == id).first()

    if auth:
        db.session.delete(auth)
        db.session.commit()
        return jsonify({"message": "Auth Deleted"}), 200
    else:
        return jsonify({"message": "Auth not found"}), 404
