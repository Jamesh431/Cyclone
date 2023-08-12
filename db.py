from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUI

__all__ = ('db', 'init_db')

db = SQLAlchemy()


def init_db(app=None, db=None):
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        db.init_app(app)

    else:
        raise ValueError("Unable to init database without database and app objects")
