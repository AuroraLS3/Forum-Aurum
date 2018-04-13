from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import db
from application.forms.messageform import MessageForm
from application.models.message import Message
from application.utils.base64util import decode64, encode64

bp = Blueprint('messages', __name__, template_folder='templates')


@bp.route("/messages/")
@login_required
def messages():
    messages = Message.query.all()
    for message in messages:
        message.content = decode64(message.content)

    return render_template("forum/messages.html", messages=messages, msgMethod='POST')


@bp.route("/messages/", methods=["POST"])
@login_required
def add_msg():
    form = MessageForm(request.form)

    content = encode64(form.message.data)
    newMsg = Message(content)

    newMsg.account_id = current_user.id

    db.session().add(newMsg)
    db.session().commit()
    return redirect(url_for("messages.messages"))


@bp.route("/messages/<msg_id>/")
@login_required
def edit_msg_page(msg_id):
    old_content = decode64(Message.query.get(msg_id).content)
    form = MessageForm()
    form.message.data = old_content
    return render_template("forum/message_new.html", action=url_for('messages.edit_msg', msg_id=msg_id), form=form)


@bp.route("/messages/<msg_id>/delete")
@login_required
def delete_msg(msg_id):
    Message.query.filter_by(id=msg_id).delete()
    db.session().commit()

    return redirect(url_for("messages.messages"))


@bp.route("/messages/<msg_id>/", methods=["POST"])
@login_required
def edit_msg(msg_id):
    message = Message.query.get(msg_id)
    form = MessageForm(request.form)

    message.content = encode64(form.message.data)
    db.session().commit()

    return redirect(url_for("messages.messages"))


@bp.route("/messages/new/")
@login_required
def add_msg_page():
    return render_template("forum/message_new.html", action=url_for('messages.add_msg'), form=MessageForm())
