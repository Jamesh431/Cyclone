import marshmallow as ma
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import JSONType
from sqlalchemy_utils import ScalarListType as ListType

from db import db
from .session_repo_xref import session_repo_xref


class Sessions(db.Model):
    __tablename__ = "Sessions"

    session_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    current_repo_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Repositories.repo_id"))
    repositories = db.Column(ListType(), nullable=False)
    num_of_commits = db.Column(db.Integer(), default=1, nullable=False)
    commit_by_repo_amount = db.Column(db.Boolean(), default=True, nullable=False)  # committing by a num of repos or a num of commits
    time_frame = db.Column(JSONType(), default={"8:17": "8:17"}, nullable=False)
    latest_commit = db.Column(db.DateTime, default=datetime.utcnow)
    current_position = db.Column(db.Integer(), default=0, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    assigned_repos = db.relationship('Repositories', secondary=session_repo_xref, back_populates='assigned_sessions')
    # users = db.relationship('Users', secondary=user_sessions_xref, back_populates='sessions', lazy='dynamic')

    def __init__(self, name, current_repo, repositories, num_of_commits, commit_by_repo_amount, time_frame, current_position, active):
        self.name = name
        self.current_repo = current_repo
        self.repositories = repositories
        self.num_of_commits = num_of_commits
        self.commit_by_repo_amount = commit_by_repo_amount
        self.time_frame = time_frame
        self.current_position = current_position
        self.active = active

    # @classmethod
    # def create_session(cls):
    #     return Sessions(None, [], 0, True, {}, 0, True)

    # def __repr__(self):
    #     for user in self.users:
    #         print(f'    {user.user_id} : {user.github_username}')

    #     return (f"Session Object: \n  session_id: {self.session_id}\n  current_repo: {self.current_repo}\n  repositories: {self.repositories}\n  num_of_commits: {self.num_of_commits}\n  commit_by_repo_ammount: {self.commit_by_repo_amount}\n  time_frame: {self.time_frame}\n  latest_commit: {self.latest_commit}\n  current_position: {self.current_position}\n  active: {self.active}\n  Users:")


class SessionSchema(ma.Schema):
    class Meta:
        fields = ['name', 'session_id', 'current_repo_id', 'repositories', 'num_of_commits', 'commit_by_repo_amount', 'time_frame', 'latest_commit', 'current_position', 'active', 'assigned_repos']

        # users = ma.fields.Nested('UserSchema', many=True, only=['user_id', 'github_username'])
        assigned_repos = ma.fields.Nested('RepoSchema', many=True)


session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)
