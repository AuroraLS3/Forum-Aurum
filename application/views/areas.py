from flask import Blueprint, g, render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import db
from application.forms.topicform import TopicForm
from application.models.area import Area
from application.models.message import Message
from application.models.topic import Topic
from application.utils.breadcrumb import Crumb

bp = Blueprint('area', __name__, template_folder='templates', url_prefix='/forum/<area_name>')


@bp.url_value_preprocessor
def fetch_area(endpoint, values):
    g.area = Area.query.filter_by(name=values.pop('area_name')).first()
    g.breadcrumbs = [
        Crumb('Home', url_for('forum.forum_main')),
        Crumb(g.area.name)
    ]


@bp.route("/")
@login_required
def area():
    if not g.area:
        return redirect(url_for("forum.forum_main"))

    return render_template("forum/area.html")


@bp.route("/topic/new/")
@login_required
def create_topic_page():
    g.breadcrumbs = [
        Crumb('Home', url_for('forum.forum_main')),
        Crumb(g.area.name, url_for('area.area', area_name=g.area.name))
    ]
    return render_template("forum/topic_new.html", form=TopicForm())


@bp.route("/topic/new/", methods=['POST'])
def create_topic():
    form = TopicForm(request.form)

    if not form.validate():
        return render_template("forum/topic_new.html", form=form)

    name = form.name.data

    newTopic = Topic(name, g.area.id)
    newTopic.account_id = current_user.id

    db.session().add(newTopic)
    db.session().commit()

    message = form.message.data

    newMsg = Message(message, newTopic.id)
    newMsg.account_id = current_user.id

    db.session().add(newMsg)
    db.session().commit()

    return redirect(url_for("topic.topic", area_name=g.area.name, created=newTopic.created))
