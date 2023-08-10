# import marshmallow as ma
# import uuid
# from sqlalchemy.dialects.postgresql import UUID

# from db import db


# class ExerciseTypes(db.Model):
#     __tablename__ = "ExerciseTypes"

#     type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = db.Column(db.String(), nullable=False, unique=True)
#     description = db.Column(db.String())
#     image_url = db.Column(db.String())

#     def __init__(self, name, description, image_url):
#         self.name = name
#         self.description = description
#         self.image_url = image_url

#     def new_exercise_type():
#         return ExerciseTypes("", "", "")  # if int put in a number, if bool put in true or false, respect data type


# class ExTypeSchema(ma.Schema):
#     class Meta:
#         fields = ["type_id", "name", "description", "image_url"]


# ex_type_schema = ExTypeSchema()
# ex_types_schema = ExTypeSchema(many=True)


# data type DateTime for db.column
# copy from orgs

import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
from datetime import datetime, timedelta
from .users import UsersSchema


# class Auths(db.Model):
#     __tablename__ = "AuthTokens"

#     auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
#     expiration = db.Column(db.DateTime(), nullable=False, default=datetime.now() + timedelta(12))

#     def __init__(self, user_id, expiration):
#         self.user_id = user_id
#         self.expiration = expiration

#     def new_auth():
#         return Auths(0, "")


# class AuthsSchema(ma.Schema):
#     class Meta:
#         fields = ['auth_token', 'user_id', 'expiration']

#         user_id = ma.fields.Nested(UsersSchema)
#         # user = ma.fields.Nested(UsersSchema(only=("role", "first_name", "user_id")))


# auth_schema = AuthsSchema()
# auths_schema = AuthsSchema(many=True)
