import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
from models.sessions import Sessions
from models.users import Users

from db import db

user_sessions_xref = db.Table("UserSessionsXref",
                              db.Model.metadata,
                              db.Column("session_id",
                                        UUID(as_uuid=True),
                                        db.ForeignKey(Sessions.session_id),
                                        primary_key=True),
                              db.Column("receiver_id",
                                        UUID(as_uuid=True),
                                        db.ForeignKey(Users.user_id),
                                        primary_key=True))
