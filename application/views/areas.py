from flask import Blueprint, g, render_template, request, url_for, redirect
from flask_login import current_user

from application import db, login_required
from application.forms.topicform import TopicForm
from application.models.area import Area
from application.models.message import Message
from application.models.topic import Topic
from application.utils.breadcrumb import Crumb

bp = Blueprint('area', __name__, template_folder='templates', url_prefix='/forum/<area_name>')


@bp.url_value_preprocessor
def fetch_area(endpoint, values):
    g.area = Area.query.filter_by(name=values.pop('area_name')).first()
    if not g.area:
        return
    g.required_role = g.area.required_role.name
    g.breadcrumbs = [
        Crumb('Home', url_for('forum.forum_main')),
        Crumb(g.area.name)
    ]


@bp.before_request
def possible_redirect(f=None):
    if not g.area:
        return redirect(url_for("forum.forum_main"))


@bp.route("/")
@login_required()
def area():
    return render_template("forum/area.html")


@bp.route("/topic/new/")
@login_required()
def create_topic_page():
    g.breadcrumbs = [
        Crumb('Home', url_for('forum.forum_main')),
        Crumb(g.area.name, url_for('area.area', area_name=g.area.name))
    ]
    return render_template("forum/topic_new.html", form=TopicForm())


@bp.route("/topic/new/", methods=['POST'])
@login_required()
def create_topic():
    form = TopicForm(request.form)

    if not form.validate():
        return render_template("forum/topic_new.html", form=form)

    name = form.name.data

    new_topic = Topic(name, g.area.id)
    new_topic.account_id = current_user.id

    db.session().add(new_topic)
    db.session().commit()

    message = form.message.data

    # Remove possible ghost messages because SQLAlchemy reuses ids
    Message.query.filter_by(topic_id=new_topic.id).delete()

    new_msg = Message(message, new_topic.id)
    new_msg.account_id = current_user.id

    db.session().add(new_msg)
    db.session().commit()

    return redirect(url_for("topic.topic", area_name=g.area.name, created=new_topic.created))
