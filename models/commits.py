import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Commits(db.Model):
    __tablename__ = "Commmits"

    commit_id = db.Column(db.String(), primary_key=True, nullable=False)
    repo_id = db.Column(db.String(), db.ForeignKey("Repositories.repo_id"), nullable=False)
    comment = db.Column(db.String(), nullable=False)
    position = db.Column(db.Integer(), nullable=False, default=0)

    def __init__(self, commit_it, repo_id, comment, position):
        self.commit_it = commit_it
        self.repo_id = repo_id
        self.comment = comment
        self.position = position

    def new_commit():
        return Commits("", "", "", 0)


class CommitSchema(ma.Schema):
    class Meta:
        fields = ["commit_id", "repo_id", "comment", "position"]

        repo_id = ma.fields.Nested("RepoSchema")


commit_schema = CommitSchema()
commits_schema = CommitSchema(many=True)
