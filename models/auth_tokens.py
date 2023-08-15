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
from .users import UserSchema


class Auths(db.Model):
    __tablename__ = "AuthTokens"

    github_token = db.Column(db.String(), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)

    def __init__(self, github_token, user_id):
        self.github_token = github_token
        self.user_id = user_id

    def new_auth():
        return Auths("", "")


class AuthsSchema(ma.Schema):
    class Meta:
        fields = ['github_token', 'user_id']

        user_id = ma.fields.Nested(UserSchema)
        # user = ma.fields.Nested(UsersSchema(only=("role", "first_name", "user_id")))


auth_schema = AuthsSchema()
auths_schema = AuthsSchema(many=True)
