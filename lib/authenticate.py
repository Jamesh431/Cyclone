import functools
from flask import Response
from datetime import datetime
from github import Github
import os

from db import db
from models.auth_tokens import Auths
from models.users import Users


def validate_token(args):
    auth_token = args.headers['auth']

    if not auth_token:
        return False

    existing_token = db.session.query(Auths).filter(Auths.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now():
            return existing_token
    else:
        return False


def fail_response():
    return Response("Authentication Required", 401)


def fail_perm_response():
    return Response("Invalid GitHub Token", 403)


def auth_with_return(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])

        if auth_info:
            kwargs["auth_info"] = auth_info
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return


def auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])

        if not auth_info:
            return fail_response()

        user_object = db.session.query(Users).filter(Users.github_username == auth_info.github_username).first()

        if not user_object.role == "admin":
            return fail_perm_response()

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_perm_response()
    return wrapper_auth_return
