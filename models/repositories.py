import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import ScalarListType as ListType

from db import db
from .users import UserSchema
# from .session_repo_xref import session_repo_xref


class Repositories(db.Model):
    __tablename__ = "Repositories"

    repo_id = db.Column(db.String(), primary_key=True, nullable=False)
    senders_github_username = db.Column(db.String(), db.ForeignKey("Users.github_username"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    ssh_key = db.Column(db.String(), nullable=False)
    branches = db.Column(ListType())
    active = db.Column(db.Boolean(), default=True, nullable=False)

    # assigned_sessions = db.relationship('Sessions', secondary=session_repo_xref, back_populates='assigned_repos')

    def __init__(self, repo_id, senders_github_username, name, ssh_key, branches, active):
        self.repo_id = repo_id
        self.senders_github_username = senders_github_username
        self.name = name
        self.ssh_key = ssh_key
        self.branches = branches
        self.active = active

    def new_repository():
        return Repositories("", "", "", "", "", True)


class RepoSchema(ma.Schema):
    class Meta:
        fields = ['repo_id', 'senders_github_username', 'name', 'ssh_key', 'branches', 'active']

        senders_github_username = ma.fields.Nested(UserSchema)
        # assigned_sessions = ma.fields.Nested('SessionSchema', many=True, only=['session_id', 'name', 'active'])


repo_schema = RepoSchema()
repos_schema = RepoSchema(many=True)
