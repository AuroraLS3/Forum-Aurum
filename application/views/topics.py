from flask import Blueprint, g, render_template, redirect, url_for

from application.models.area import Area
from application.models.topic import Topic

bp = Blueprint('topic', __name__, template_folder='templates', url_prefix='/forum/<area_name>/<topic_name>')


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    area = Area.query.filter_by(name=values.pop('area_name')).first()
    if not area:
        return redirect(url_for("forum.forum_main"))

    topic = Topic.query.filter_by(area_id=area.id, name=values.pop('topic_name')).first()

    if not topic:
        return redirect(url_for("area.area", area_name=area.name))

    g.area = area
    g.topic = topic


@bp.route("/")
def topic():
    return render_template("forum/topic.html")
