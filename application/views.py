# coding=utf-8
import bcrypt
from flask import redirect, render_template, request, url_for

from application import app, db
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
    return render_template("newmessage.html", action=url_for('edit_msg', msg_id=msg_id))


@app.route("/messages/<msg_id>/", methods=["POST"])
def edit_msg(msg_id):
    message = Message.query.get(msg_id)
    message.content = encode64(request.form.get("message"))
    db.session().commit()

    return redirect(url_for("messages"))


@app.route("/messages/new/")
def add_msg_page():
    return render_template("newmessage.html", action=url_for('add_msg'))


@app.route("/register/")
def register_page():
    return render_template("register.html")


@app.route("/register/", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password").encode()
    passwordAgain = request.form.get("passwordAgain").encode()
    hashpw = bcrypt.hashpw(password, bcrypt.gensalt())
    if (bcrypt.checkpw(passwordAgain, hashpw)):
        registeringUser = User(username, hashpw)

        db.session().add(registeringUser)
        db.session().commit()

        return "Created new user '{0}!'".format(username)
    else:
        return "Passwords didn't match"
