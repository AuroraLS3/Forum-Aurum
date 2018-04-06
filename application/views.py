# coding=utf-8
import bcrypt
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

from application import app, db
from application.forms.loginform import LoginForm
from application.forms.messageform import MessageForm
from application.forms.registerform import RegisterForm
from application.models.message import Message
from application.models.user import User
from application.utils.base64util import encode64, decode64


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/users/")
@login_required
def users():
    users = User.query.all()
    for user in users:
        user.username = user.username
        user.password = user.password.decode()
    return render_template("users.html", users=users)


@app.route("/messages/")
@login_required
def messages():
    messages = Message.query.all()
    for message in messages:
        message.content = decode64(message.content)

    return render_template("messages.html", messages=messages, msgMethod='POST')


@app.route("/messages/", methods=["POST"])
@login_required
def add_msg():
    form = MessageForm(request.form)

    content = encode64(form.content.data)
    newMsg = Message(content)

    newMsg.account_id = current_user.id

    db.session().add(newMsg)
    db.session().commit()
    return redirect(url_for("messages"))


@app.route("/messages/<msg_id>/")
@login_required
def edit_msg_page(msg_id):
    old_content = decode64(Message.query.get(msg_id).content)
    form = MessageForm()
    form.content.data = old_content
    return render_template("newmessage.html", action=url_for('edit_msg', msg_id=msg_id), form=form)


@app.route("/messages/<msg_id>/", methods=["POST"])
@login_required
def edit_msg(msg_id):
    message = Message.query.get(msg_id)
    form = MessageForm(request.form)

    message.content = encode64(form.content.data)
    db.session().commit()

    return redirect(url_for("messages"))


@app.route("/messages/new/")
@login_required
def add_msg_page():
    return render_template("newmessage.html", action=url_for('add_msg'), form=MessageForm())


@app.route("/register/")
def register_page():
    return render_template("auth/register.html", form=RegisterForm())


@app.route("/register/", methods=["POST"])
def register():
    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/register.html", form=form)

    username = form.username.data
    password = form.password.data.encode()

    hashpw = bcrypt.hashpw(password, bcrypt.gensalt())
    registeringUser = User(username, hashpw)

    db.session().add(registeringUser)
    db.session().commit()

    return "Created new user '{0}!'".format(username)


@app.route("/auth/login/")
def login_page():
    return render_template("auth/login.html", form=LoginForm())


@app.route("/auth/logout/")
def logout():
    logout_user()
    return redirect(url_for("hello"))


@app.route("/auth/login/", methods=["POST"])
def login():
    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/login.html", form=form)

    username = form.username.data

    user = User.query.filter_by(username=username).first()

    if user is None:
        return render_template("auth/login.html", form=form, error="User doesn't exist")

    password = form.password.data.encode()
    correctPass = bcrypt.checkpw(password, user.password)

    if not correctPass:
        return render_template("auth/login.html", form=form, error="Incorrect Password")

    login_user(user)
    return redirect(url_for("hello"))
