import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import ScalarListType as ListType

from db import db
from .users import UserSchema
# from .session_repo_xref import session_repo_xref


class Repositories(db.Model):
    __tablename__ = "Repositories"

    repo_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    ssh_key = db.Column(db.String(), nullable=False)
    branches = db.Column(ListType())
    active = db.Column(db.Boolean(), default=True, nullable=False)

    # assigned_sessions = db.relationship('Sessions', secondary=session_repo_xref, back_populates='assigned_repos')

    def __init__(self, sender_id, name, ssh_key, branches, active):
        self.sender_id = sender_id
        self.name = name
        self.ssh_key = ssh_key
        self.branches = branches
        self.active = active

    def new_repository():
        return Repositories("", "", "", "", True)


class RepoSchema(ma.Schema):
    class Meta:
        fields = ['repo_id', 'sender_id', 'name', 'ssh_key', 'branches', 'active']

        sender_id = ma.fields.Nested(UserSchema)
        # assigned_sessions = ma.fields.Nested('SessionSchema', many=True, only=['session_id', 'name', 'active'])


repo_schema = RepoSchema()
repos_schema = RepoSchema(many=True)
