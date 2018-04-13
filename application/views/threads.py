from flask import Blueprint, g, render_template

from application.models.area import Area

bp = Blueprint('thread', __name__, template_folder='templates', url_prefix='/<area_name>/<thread_name>')


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.area = Area.query.filter_by(name=values.pop('area_name').replace("%20", " "))
    g.thread = Area.query.filter_by(area_id=g.area.id, name=values.pop('thread_name').replace("%20", " "))


@bp.route("/")
def area():
    return render_template("thread.html")
