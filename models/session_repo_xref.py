from db import db

session_repo_xref = db.Table(
    "SessionRepoXref",
    db.Model.metadata,
    db.Column('session_id', db.ForeignKey('Sessions.session_id'), primary_key=True),
    db.Column('repo_id', db.ForeignKey('Repositories.repo_id'), primary_key=True)
)
