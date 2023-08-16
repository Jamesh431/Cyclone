import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import ScalarListType as ListType

from db import db
from .users import UserSchema


class Repositories(db.Model):
    __tablename__ = "Repositories"

    repo_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    branches = db.Column(ListType())

    def __init__(self, sender_id, name, branches):
        self.sender_id = sender_id
        self.name = name
        self.branches = branches

    def new_repository():
        return Repositories("", "", [])


class RepoSchema(ma.Schema):
    class Meta:
        fields = ['repo_id', 'sender_id', 'name', 'branches']

        user_id = ma.fields.Nested(UserSchema)


repo_schema = RepoSchema()
repos_schema = RepoSchema(many=True)
