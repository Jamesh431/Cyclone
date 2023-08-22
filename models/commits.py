import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

from db import db


class Commits(db.Model):
    __tablename__ = "Commmits"

    commit_id = db.Column(db.String(), primary_key=True, nullable=False)
    repo_id = db.Column(db.String(), nullable=False, unique=True)
    comment = db.Column(db.String(), nullable=False)
    position = db.Column(db.Integer(), nullable=False, unique=True, default=0)

    def __init__(self, repo_id, comment, position):
        self.repo_id = repo_id
        self.comment = comment
        self.position = position

    def new_commit():
        return Commits("", "", 0)


class CommitSchema(ma.Schema):
    class Meta:
        fields = ["commit_id", "repo_id", "comment", "position"]


commit_schema = CommitSchema()
commits_schema = CommitSchema(many=True)
