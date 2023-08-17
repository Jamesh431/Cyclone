from flask import Flask, request, jsonify
from db import *
from flask_marshmallow import Marshmallow

import os
from models.auth_tokens import Auths
from models.users import Users
from models.sessions import Sessions
from models.repositories import Repositories
from models.commits import Commits
from models.user_sessions_xref import user_sessions_xref
import routes

database_pre = os.environ.get("DATABASE_PRE")
database_user = os.environ.get("DATABASE_USER")
database_addr = os.environ.get("DATABASE_ADDR")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_user}@{database_addr}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)
ma = Marshmallow(app)


def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("Tables created")


app.register_blueprint(routes.users)
app.register_blueprint(routes.repositories)
app.register_blueprint(routes.sessions)
# app.register_blueprint(routes.)
# app.register_blueprint(routes.)


if __name__ == "__main__":
    create_all()
    app.run(port=8086, host="0.0.0.0", debug=True)
