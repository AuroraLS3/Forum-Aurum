# coding=utf-8
import bcrypt
from flask import redirect, render_template, request, url_for

from application import app, db
from application.forms.registerform import RegisterForm
from application.models.message import Message
from application.models.user import User
from application.utils.base64util import encode64, decode64


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/users/")
def users():
    users = User.query.all()
    for user in users:
        user.username = user.username
        user.password = user.password.decode()
    return render_template("users.html", users=users)


@app.route("/messages/")
def messages():
    messages = Message.query.all()
    for message in messages:
        message.content = decode64(message.content)

    return render_template("messages.html", messages=messages, msgMethod='POST')


@app.route("/messages/", methods=["POST"])
def add_msg():
    msg = request.form.get("message")
    content = encode64(msg)
    newMsg = Message(content)
    db.session().add(newMsg)
    db.session().commit()
    return redirect(url_for("messages"))


@app.route("/messages/<msg_id>/")
def edit_msg_page(msg_id):
    old_content = decode64(Message.query.get(msg_id).content)
    return render_template("newmessage.html", action=url_for('edit_msg', msg_id=msg_id), value=old_content)


@app.route("/messages/<msg_id>/", methods=["POST"])
def edit_msg(msg_id):
    message = Message.query.get(msg_id)
    message.content = encode64(request.form.get("message"))
    db.session().commit()

    return redirect(url_for("messages"))


@app.route("/messages/new/")
def add_msg_page():
    return render_template("newmessage.html", action=url_for('add_msg'), value="")


@app.route("/register/")
def register_page():
    return render_template("register.html", form=RegisterForm())


@app.route("/register/", methods=["POST"])
def register():
    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("register.html", form=form)

    username = form.username.data
    password = form.password.data.encode()

    hashpw = bcrypt.hashpw(password, bcrypt.gensalt())
    registeringUser = User(username, hashpw)

    db.session().add(registeringUser)
    db.session().commit()

    return "Created new user '{0}!'".format(username)
