from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user

from application import db, login_required
from application.forms.roleform import RoleForm, RoleFormAdmin
from application.models.message import Message
from application.models.role import Role
from application.models.topic import Topic
from application.models.user import User

bp = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')


@bp.route("/")
@login_required(role='moderator')
def users():
    users = User.query.all()
    for user in users:
        user.name = user.name
        if current_user.is_authenticated and current_user.hasRole('admin'):
            print("ROLEFORM_ADMIN")
            user.form = RoleFormAdmin()
        else:
            print("ROLEFORM")
            user.form = RoleForm()

    return render_template("users/list.html", users=users)


@bp.route("/<user_name>/", methods=["POST"])
@login_required(role='moderator')
def edit(user_name):
    form = RoleFormAdmin(request.form)
    user = User.query.filter_by(name=user_name).first()

    isAdmin = current_user.hasRole('admin')

    newRoles = list(map(lambda role: Role.query.filter_by(id=role.id).first(), form.roles.data))
    if (Role.query.filter_by(name='admin') in newRoles or Role.query.filter_by(
            name='moderator') in newRoles) and not isAdmin:
        return render_template("users/list.html", users=User.query.all(),
                               error="You can't modify admin or moderator users if you are not an admin!")

    user.roles = newRoles
    db.session().commit()
    return redirect(url_for("users.users"))


@bp.route("/delete/<user_name>/")
@login_required(role='moderator')
def delete(user_name):
    user = User.query.filter_by(name=user_name).first()
    user_id = user.id

    if 'admin' in list(map(lambda role: role.name, user.roles)):
        return redirect(url_for("users.users"))

    user.roles = [Role.query.filter_by(name='guest').first()]
    db.session().commit()

    Message.query.filter_by(account_id=user_id).delete()
    Topic.query.filter_by(account_id=user_id).delete()
    User.query.filter_by(name=user_name).delete()

    db.session().commit()
    return redirect(url_for("users.users"))
