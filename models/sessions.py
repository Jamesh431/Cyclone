import marshmallow as ma
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import JSONType
from sqlalchemy_utils import ScalarListType as ListType

from db import db
from .repositories import RepoSchema
from .user_sessions_xref import user_sessions_xref
# from .users import UserSchema


class Sessions(db.Model):
    __tablename__ = "Sessions"

    session_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_repo = db.Column(UUID(as_uuid=True), db.ForeignKey("Repositories.repo_id"))
    repositories = db.Column(ListType(), nullable=False)
    num_of_commits = db.Column(db.Integer(), default=1, nullable=False)
    commit_by_repo_ammount = db.Column(db.Boolean(), default=True, nullable=False)  # committing by a num of repos or a num of commits
    time_frame = db.Column(JSONType(), default={"8:17": "8:17"}, nullable=False)
    latest_commit = db.Column(db.DateTime, default=datetime.utcnow)
    current_position = db.Column(db.Integer(), default=0, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    user = db.relationship('Users', secondary=user_sessions_xref, back_populates='session')

    def __init__(self, current_repo, repositories, num_of_commits, commit_by_repo_ammount, time_frame, current_position, active):
        self.current_repo = current_repo
        self.repositories = repositories
        self.num_of_commits = num_of_commits
        self.commit_by_repo_ammount = commit_by_repo_ammount
        self.time_frame = time_frame
        self.current_position = current_position
        self.active = active

    def new_session():
        return Sessions("", [], 0, True, {}, 0, True)


class SesssionSchema(ma.Schema):
    class Meta:
        fields = ['session_id', 'current_repo', 'repositories', 'num_of_commits', 'commit_by_repo_amount', 'time_to_commit', 'time_frame', 'latest_commit', 'current_position', 'active', "user"]

        current_repo = ma.fields.Nested(RepoSchema)
        user = ma.fields.Nested("Users", only=["user_id", "github_username"])


session_schema = SesssionSchema()
sessions_schema = SesssionSchema(many=True)
