from flask import Blueprint, render_template
from flask_login import login_required

from application.models.user import User

bp = Blueprint('users', __name__, template_folder='templates')


@bp.route("/users/")
@login_required
def users():
    users = User.query.all()
    for user in users:
        user.username = user.username
        user.password = user.password.decode()
    return render_template("users.html", users=users)
