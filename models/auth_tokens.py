import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Auths(db.Model):
    __tablename__ = "AuthTokens"

    github_token = db.Column(db.String(), primary_key=True, unique=True)
    github_username = db.Column(db.String(), db.ForeignKey("Users.github_username"), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, github_token, github_username, active):
        self.github_token = github_token
        self.github_username = github_username
        self.active = active if active else True

    def new_auth():
        return Auths("", "", True)


class AuthsSchema(ma.Schema):
    class Meta:
        fields = ['github_token', 'github_username', 'active']

        github_username = ma.fields.Nested("UserSchema")


auth_schema = AuthsSchema()
auths_schema = AuthsSchema(many=True)
