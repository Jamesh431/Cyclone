import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
# from .user_sessions_xref import user_sessions_xref


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_username = db.Column(db.String(), nullable=False, unique=True)
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
        fields = ["user_id", "github_username", "cyclone_pass", "active"]


user_schema = UserSchema()
users_schema = UserSchema(many=True)
