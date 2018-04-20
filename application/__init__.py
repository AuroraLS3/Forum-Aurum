# coding=utf-8
import os
from functools import wraps
from os import urandom

from flask import Flask, g
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap
from flask_misaka import Misaka

from application.utils.CustomMisakaRenderer import CustomMisakaRenderer

app = Flask(__name__)
Bootstrap(app)
Misaka(app, renderer=CustomMisakaRenderer())

from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


def login_required(role="anyone"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            req_role = role
            if not current_user.is_authenticated():
                return login_manager.unauthorized()

            if g.required_role is not None:
                req_role = g.required_role

            unauthorized = False

            if req_role is not "anyone":
                unauthorized = not current_user.hasRole(role)

            if unauthorized:
                return login_manager.unauthorized()

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


from application.views import forum, users, auth, areas, topics

app.register_blueprint(auth.bp)
app.register_blueprint(forum.bp)
app.register_blueprint(users.bp)
app.register_blueprint(areas.bp)
app.register_blueprint(topics.bp)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login_page"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from application.models.user import User
from application.models.message import Message
from application.models.topic import Topic
from application.models.area import Area
from application.models.role import Role

app.config["SECRET_KEY"] = urandom(32)

db.create_all()

if not Role.query.filter_by(name='anyone').first():
    db.session.add(Role('anyone'))
    db.session.add(Role('guest'))
    db.session.add(Role('member'))
    db.session.add(Role('moderator'))
    db.session.add(Role('admin'))
    db.session.commit()
