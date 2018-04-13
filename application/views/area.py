from flask import Blueprint, g, render_template

from application.models.area import Area

bp = Blueprint('area', __name__, template_folder='templates', url_prefix='/<area_name>')


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.area_name = values.pop('area_name').replace("%20", " ")


@bp.route("/")
def area():
    area = Area.query.filter_by(id=g.area_name)
    return render_template("area.html", area=area)
