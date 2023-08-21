import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Auths(db.Model):
    __tablename__ = "AuthTokens"

    github_token = db.Column(db.String(), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, github_token, user_id, active):
        self.github_token = github_token
        self.user_id = user_id
        self.active = active

    def new_auth():
        return Auths("", "", True)


class AuthsSchema(ma.Schema):
    class Meta:
        fields = ['github_token', 'user_id', 'active']

        user_id = ma.fields.Nested("UserSchema")


auth_schema = AuthsSchema()
auths_schema = AuthsSchema(many=True)
