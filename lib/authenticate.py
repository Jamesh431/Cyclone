import functools
from flask import Response
from datetime import datetime
from github import Github
import os

from db import db
from models.auth_tokens import Auths
from models.users import Users


def fail_response():
    return Response("Authentication Required", 401)


def fail_perm_response():
    return Response("Invalid GitHub Token", 403)


def validate_github_token(args):
    github_info = args.headers['github_info'].split(",")
    github_token = github_info[0]
    github_username = github_info[1]

    auth_check = db.session.query(Auths).filter(Auths.github_token == github_token).first()

    if not auth_check:
        return False

    try:
        Github(github_token).get_user(github_username)
        return auth_check
    except:
        db.session.delete(auth_check)
        db.session.commit()
        return fail_perm_response()


def auth_with_return(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_github_token(args[0])
        kwargs["auth_info"] = auth_info

        return func(*args, **kwargs) if auth_info else fail_response()

    return wrapper_auth_return


def auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_github_token(args[0])
        kwargs["auth_info"] = auth_info

        return func(*args, **kwargs) if auth_info else fail_response()

    return wrapper_auth_return
