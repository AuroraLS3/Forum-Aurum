from flask import Blueprint, redirect, url_for, render_template, request, g

from application import db, login_required
from application.forms.areaform import AreaForm
from application.models.area import Area
from application.models.message import Message
from application.models.role import Role
from application.models.topic import Topic
from application.utils.breadcrumb import Crumb

bp = Blueprint('forum', __name__, template_folder='templates')


@bp.url_value_preprocessor
def breadcrumb(endpoint, values):
    g.breadcrumbs = [Crumb('Home')]


@bp.route("/")
def hello():
    return redirect(url_for("forum.forum_main"))


@bp.route("/forum/")
def forum_main():
    areas = Area.query.all()
    most_active_area = Area.find_area_with_most_messages()
    message_count = Message.find_message_count()
    hot_topic = Topic.find_hot_topic()
    topic_count = Topic.find_topic_count()
    return render_template("forum.html",
                           areas=areas,
                           most_active_area=most_active_area,
                           message_count=message_count,
                           hot_topic=hot_topic,
                           topic_count=topic_count)


@bp.route("/area/new/")
@login_required(role='moderator')
def create_area_page():
    g.breadcrumbs = [Crumb('Home', url_for("forum.forum_main"))]
    form = AreaForm()
    form.role.choices = [(role.id, role.name) for role in Role.query.order_by('id')]

    return render_template("forum/area_new.html", action=url_for('forum.create_area'), form=form)


@bp.route("/area/new/", methods=["POST"])
@login_required(role='moderator')
def create_area():
    form = AreaForm(request.form)

    if not form.validate():
        return render_template("forum/area_new.html", form=form)

    name = form.name.data
    description = form.description.data

    new_area = Area(name, description, form.role.data.id)

    db.session().add(new_area)
    db.session().commit()

    return redirect(url_for("area.area", area_name=name))
