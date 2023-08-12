import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.sessions import SesssionSchema
from models.users import UserSchema


class UserSessionsXref(db.model):
    __tablename__ = "UserSessionsXref"

    session_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Sessions.session_id"), primary_key=True)
    receiver_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), primary_key=True)
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), primary_key=True)

    def __init__(self, session_id, receiver_id, sender_id):
        self.session_id = session_id
        self.receiver_id = receiver_id
        self.sender_id = sender_id

    def new_user_session_xref():
        return UserSessionsXref("", "", "")


class UserSessionsXrefSchema(ma.Schema):
    class Meta:
        fields = ["session_id", "receiver_id", "sender_id"]

        session_id = ma.fields.Nested(SesssionSchema)
        receiver_id = ma.fields.Nested(UserSchema)
        sender_id = ma.fields.Nested(UserSchema)


user_session_xref = UserSessionsXrefSchema()
user_session_xrefs = UserSessionsXrefSchema(many=True)
