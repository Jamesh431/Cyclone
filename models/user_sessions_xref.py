import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db

user_sessions_xref = db.Table("UserSessionsXref",
                              db.Model.metadata,
                              session_id=db.Column(UUID(as_uuid=True), db.ForeignKey("Sessions.session_id"), primary_key=True),
                              receiver_id=db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), primary_key=True),
                              sender_id=db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), primary_key=True))
