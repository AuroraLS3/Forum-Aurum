# coding=utf-8
import os
from os import urandom

from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views
from application.models.user import User
from application.models.message import Message
from application.models.thread import Thread
from application.models.area import Area
from application.models.role import Role

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_page"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.create_all()
