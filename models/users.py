import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_username = db.Column(db.String(), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def new_exercise_type():
        return Users("", "")


class UsersSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "github_username"]


user_schema = UsersSchema()
user_schema = UsersSchema(many=True)
