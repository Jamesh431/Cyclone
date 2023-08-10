import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import date
from db import db


class Commits(db.Model):
    __tablename__ = "Commmits"

    commit_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_id = db.Column(db.String(), nullable=False, unique=True)
    comment = db.Column(db.String(), nullable=False)
    position = db.Column(db.Integer(), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def new_commit():
        return Commits("", "", "", 0)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "github_username"]


user_schema = UsersSchema()
user_schema = UsersSchema(many=True)
