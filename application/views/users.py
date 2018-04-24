from flask import Blueprint, render_template, url_for, redirect, request

from application import db, login_required
from application.forms.roleform import RoleForm
from application.models.role import Role
from application.models.user import User

bp = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')


@bp.route("/")
@login_required(role='moderator')
def users():
    users = User.query.all()
    for user in users:
        user.name = user.name
        user.password = user.password.decode()
        role_form = RoleForm()
        user.form = role_form
    return render_template("users/list.html", users=users)


@bp.route("/<user_name>/", methods=["POST"])
@login_required(role='moderator')
def edit(user_name):
    form = RoleForm(request.form)
    user = User.query.filter_by(name=user_name).first()

    if not form.validate():
        user.form = form
        return render_template("users/list.html", users=[user])

    user.roles = list(map(lambda role: Role.query.filter_by(id=role.id).first(), form.roles.data))
    db.session().commit()
    return redirect(url_for("users.users"))


@bp.route("/delete/<user_name>/")
@login_required(role='moderator')
def delete(user_name):
    User.query.filter_by(name=user_name).delete()
    db.session().commit()
    return redirect(url_for("users.users"))
