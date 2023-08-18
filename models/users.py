import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
# from .user_sessions_xref import user_sessions_xref


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_username = db.Column(db.String(), nullable=False, unique=True)

    # sessions = db.relationship('Sessions', secondary=user_sessions_xref, back_populates='users', lazy='dynamic')

    def __init__(self, github_username):
        self.github_username = github_username

    def new_user():
        return Users("")


class UserSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "github_username"]

        # sessions = ma.fields.Nested("SessionSchema", many=True, exclude=("users",))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
