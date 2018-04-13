# coding=utf-8
import os
from os import urandom

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application.views import forum, users, messages, auth, areas, threads

app.register_blueprint(auth.bp)
app.register_blueprint(forum.bp)
app.register_blueprint(users.bp)
app.register_blueprint(areas.bp)
app.register_blueprint(threads.bp)
app.register_blueprint(messages.bp)

from application.models.user import User
from application.models.message import Message
from application.models.thread import Thread
from application.models.area import Area
from application.models.role import Role

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login_page"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.create_all()
