from flask import Blueprint, g, render_template, redirect, url_for

from application.models.area import Area
from application.models.thread import Thread

bp = Blueprint('thread', __name__, template_folder='templates', url_prefix='/forum/<area_name>/<thread_name>')


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    area = Area.query.filter_by(name=values.pop('area_name')).first()
    thread = Thread.query.filter_by(area_id=area.id, name=values.pop('thread_name')).first()

    g.area = area
    g.thread = thread
    if not area:
        return redirect(url_for("forum.forum_main"))
    if not thread:
        return redirect(url_for("area.area", area_name=area.name))


@bp.route("/")
def thread():
    return render_template("forum/thread.html")
