from models.repositories import RepoSchema
from models.sessions import SessionSchema
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

# session_repo_xref = db.Table(
#     "SessionRepoXref",
#     db.Column('session_id', db.ForeignKey('Sessions.session_id'), primary_key=True),
#     db.Column('repo_id', db.ForeignKey('Repositories.repo_id'), primary_key=True)
# )


class SessionRepoXref(db.Model):
    __tablename__ = "SessionRepoXref"

    session_id = db.Column(db.String(), db.ForeignKey("Sessions.session_id"), primary_key=True)
    repo_id = db.Column(db.String(), db.ForeignKey("Repositories.repo_id"), primary_key=True)

    def __init__(self, session_id, repo_id):
        self.session_id = session_id
        self.repo_id = repo_id

    def new_session_repo_xref():
        return SessionRepoXref("", "")


class SessionRepoXrefSchema(ma.Schema):
    class Meta:
        fields = ["session_id", "repo_id"]

        session_id = ma.fields.Nested(SessionSchema())
        repo_id = ma.fields.Nested(RepoSchema())


session_repo_xref = SessionRepoXrefSchema()
session_repo_xrefs = SessionRepoXrefSchema(many=True)
