import marshmallow as ma
import uuid
from datetime import datetime, time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import JSONType

from models.repositories import RepositoriesSchema
from db import db


class Sessions(db.model):
    __tablename__ = "Sessions"

    session_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_repo = db.Column(UUID(as_uuid=True), db.ForeignKey("Repositories.repo_id"))
    num_of_commits = db.Column(db.integer(), default=1, nullable=False)
    commit_by_repo_ammount = db.Column(db.Boolean(), default=True, nullable=False)  # committing by a num of repos or a num of commits
    time_to_commit = db.Column(db.DateTime.time())  # default=datetime.combine(datetime.min, time(8, 17)
    time_frame = db.Column(db.JSONType(), default={"8:17": "8:17"}, nullable=False)
    latest_commit = db.Column(db.DateTime())
    current_position = db.Column(db.integer(), default=0, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, current_repo, num_of_commits, commit_by_repo_ammount, time_to_commit, time_frame, latest_commit, current_position, active):
        self.current_repo = current_repo
        self.num_of_commits = num_of_commits
        self.commit_by_repo_ammount = commit_by_repo_ammount
        self.time_to_commit = time_to_commit
        self.time_frame = time_frame
        self.latest_commit = latest_commit
        self.current_position = current_position
        self.active = active

    def new_session():
        return Sessions("", "", "", 1, True, "", {}, "", 0, True)


class SesssionsSchema(ma.Schema):
    class Meta:
        fields = ['session_id', 'current_repo', 'num_of_commits', 'commit_by_repo_amount', 'time_to_commit', 'time_frame', 'latest_commit', 'current_position', 'active']

        current_repo = ma.fields.Nested(RepositoriesSchema)


session_schema = SesssionsSchema()
sessions_schema = SesssionsSchema(many=True)
