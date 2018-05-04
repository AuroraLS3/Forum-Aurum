from flask import Blueprint, g, render_template, redirect, url_for, request
from flask_login import current_user

from application import db, login_required
from application.forms.messageform import MessageForm
from application.models.area import Area
from application.models.message import Message
from application.models.topic import Topic
from application.utils.breadcrumb import Crumb

bp = Blueprint('topic', __name__, template_folder='templates', url_prefix='/forum/<area_name>/<created>')


@bp.url_value_preprocessor
def fetch_area_and_topic(endpoint, values):
    g.area = Area.query.filter_by(name=values.pop('area_name')).first()
    if not g.area:
        return
    g.required_role = g.area.required_role.name

    g.topic = Topic.query.filter_by(area_id=g.area.id, created=values.pop('created')).first()

    if not g.topic:
        return

    g.breadcrumbs = [
        Crumb('Home', url_for('forum.forum_main')),
        Crumb(g.area.name, url_for('area.area', area_name=g.area.name)),
        Crumb(g.topic.name)
    ]


@bp.before_request
def possible_redirect(f=None):
    if not g.area:
        return redirect(url_for("forum.forum_main"))
    if not g.topic:
        return redirect(url_for("area.area", area_name=g.area.name))


@bp.route("/")
def topic():
    return render_template("forum/topic.html", form=MessageForm())


@bp.route("/comment/", methods=["POST"])
@login_required()
def add_msg():
    form = MessageForm(request.form)

    content = form.message.data
    new_msg = Message(content, g.topic.id)

    new_msg.account_id = current_user.id

    db.session().add(new_msg)
    db.session().commit()
    return redirect(url_for("topic.topic", area_name=g.area.name, created=g.topic.created))


@bp.route("/edit/<msg_id>/")
@login_required()
def edit_msg_page(msg_id):
    message = Message.query.get(msg_id)

    if current_user.id is not message.account_id:
        return redirect(url_for("topic", area_name=g.area.name, created=g.topic.created))

    old_content = message.content
    form = MessageForm()
    form.message.data = old_content
    return render_template("forum/message_new.html",
                           action=url_for('topic.edit_msg', msg_id=msg_id, area_name=g.area.name,
                                          created=g.topic.created), form=form)


@bp.route("/delete/<msg_id>/")
@login_required()
def delete_msg(msg_id):
    first_msg_id = g.topic.messages[0].id
    topic_id = g.topic.id

    message = Message.query.get(msg_id)

    if not (current_user.id == message.account_id or current_user.has_role('moderator')):
        return redirect(url_for("topic", area_name=g.area.name, created=g.topic.created))

    if str(first_msg_id) == str(msg_id):
        # If first message, delete topic and it's messages.
        Message.query.filter_by(topic_id=topic_id).delete()
        Topic.query.filter_by(id=topic_id).delete()
    else:
        Message.query.filter_by(id=msg_id).delete()

    db.session().commit()

    return redirect(url_for("topic.topic", area_name=g.area.name, created=g.topic.created))


@bp.route("/edit/<msg_id>/", methods=["POST"])
@login_required()
def edit_msg(msg_id):
    message = Message.query.get(msg_id)

    if current_user.id is not message.account_id:
        return redirect(url_for("topic", area_name=g.area.name, created=g.topic.created))

    form = MessageForm(request.form)

    message.content = form.message.data
    db.session().commit()

    return redirect(url_for("topic.topic", area_name=g.area.name, created=g.topic.created))
