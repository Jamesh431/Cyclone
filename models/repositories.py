import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import ScalarListType as ListType

from db import db
from models.users import UserSchema


class Repositories(db.Model):
    __tablename__ = "Repositories"

    repo_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    branches = db.Column(ListType())

    def __init__(self, user_id, name, branches):
        self.user_id = user_id
        self.name = name
        self.branches = branches

    def new_repository():
        return Repositories("", "", [])


class RepoSchema(ma.Schema):
    class Meta:
        fields = ['repo_id', 'user_id', 'name', 'branches']

        user_id = ma.fields.Nested(UserSchema)


repo_schema = RepoSchema()
repos_schema = RepoSchema(many=True)
