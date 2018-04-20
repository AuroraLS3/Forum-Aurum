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
def pull_lang_code(endpoint, values):
    area = Area.query.filter_by(name=values.pop('area_name')).first()
    if not area:
        return redirect(url_for("forum.forum_main"))
    g.required_role = g.area.required_role.name

    topic = Topic.query.filter_by(area_id=area.id, created=values.pop('created')).first()

    # topic.messages foreach msg msg.content

    if not topic:
        return redirect(url_for("area.area", area_name=area.name))

    g.area = area
    g.topic = topic
    g.breadcrumbs = [
        Crumb('Home', url_for('forum.forum_main')),
        Crumb(g.area.name, url_for('area.area', area_name=g.area.name)),
        Crumb(g.topic.name)
    ]


@bp.route("/")
def topic():
    return render_template("forum/topic.html", form=MessageForm())


@bp.route("/comment/")
@login_required()
def add_msg_page():
    return render_template("forum/message_new.html",
                           action=url_for('topic.add_msg', area_name=g.area.name, created=g.topic.created),
                           )


@bp.route("/comment/", methods=["POST"])
@login_required()
def add_msg():
    form = MessageForm(request.form)

    content = form.message.data
    newMsg = Message(content, g.topic.id)

    newMsg.account_id = current_user.id

    db.session().add(newMsg)
    db.session().commit()
    return redirect(url_for("topic.topic", area_name=g.area.name, created=g.topic.created))


@bp.route("/edit/<msg_id>/")
@login_required()
def edit_msg_page(msg_id):
    old_content = Message.query.get(msg_id).content
    form = MessageForm()
    form.message.data = old_content
    return render_template("forum/message_new.html",
                           action=url_for('topic.edit_msg', msg_id=msg_id, area_name=g.area.name,
                                          created=g.topic.created), form=form)


@bp.route("/delete/<msg_id>/")
@login_required()
def delete_msg(msg_id):
    Message.query.filter_by(id=msg_id).delete()
    db.session().commit()

    return redirect(url_for("topic.topic", area_name=g.area.name, created=g.topic.created))


@bp.route("/edit/<msg_id>/", methods=["POST"])
@login_required()
def edit_msg(msg_id):
    message = Message.query.get(msg_id)
    form = MessageForm(request.form)

    message.content = form.message.data
    db.session().commit()

    return redirect(url_for("topic.topic", area_name=g.area.name, created=g.topic.created))
