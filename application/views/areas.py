from flask import Blueprint, g, render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import db
from application.forms.threadform import ThreadForm
from application.models.area import Area
from application.models.message import Message
from application.models.thread import Thread
from application.utils.base64util import encode64

bp = Blueprint('area', __name__, template_folder='templates', url_prefix='/<area_name>')


@bp.url_value_preprocessor
def fetch_area(endpoint, values):
    g.area = Area.query.filter_by(name=values.pop('area_name').replace("%20", " "))


@bp.route("/")
@login_required
def area():
    return render_template("forum/area.html")


@bp.route("/area/new")
@login_required
def create_area_page():
    return render_template("forum/thread_new.html", action=url_for('forum.create_area'), form=ThreadForm())


@bp.route("/thread/new", methods=["POST"])
@login_required
def create_thread_page():
    form = ThreadForm(request.form)

    if not form.validate():
        return render_template("forum/thread_new.html", form=form)

    name = form.name.data

    newThread = Thread(name, g.area.id)
    newThread.account_id = current_user.id

    db.session().add(newThread)
    db.session().commit()

    message = encode64(form.message.data)

    newMsg = Message(message, newThread.id)
    newMsg.account_id = current_user.id

    db.session().add(newMsg)
    db.session().commit()

    return redirect(url_for("thread.thread", area_name=g.area.name, thread_name=name))
