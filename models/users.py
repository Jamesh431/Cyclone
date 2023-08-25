import marshmallow as ma

from db import db
# from .user_sessions_xref import user_sessions_xref


class Users(db.Model):
    __tablename__ = "Users"

    github_username = db.Column(db.String(), primary_key=True, nullable=False, unique=True)
    cyclone_pass = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, github_username, cyclone_pass, active):
        self.github_username = github_username
        self.cyclone_pass = cyclone_pass
        self.active = active

    def new_user():
        return Users("", "", True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ["github_username", "cyclone_pass", "active"]


user_schema = UserSchema()
users_schema = UserSchema(many=True)
