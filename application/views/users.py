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
    all_users = User.query.all()
    for user in all_users:
        user.name = user.name
        if current_user.is_authenticated and current_user.has_role('admin'):
            print("ROLEFORM_ADMIN")
            user.form = RoleFormAdmin()
        else:
            print("ROLEFORM")
            user.form = RoleForm()

    error = request.args.get('error')

    return render_template("users/list.html", users=all_users, error=error)


@bp.route("/<user_name>/", methods=["POST"])
@login_required(role='moderator')
def edit(user_name):
    form = RoleFormAdmin(request.form)
    user = User.query.filter_by(name=user_name).first()

    is_admin = current_user.has_role('admin')

    # Turn list of role names given in form into Role database objects
    new_roles = list(map(lambda role: Role.query.filter_by(id=role.id).first(), form.roles.data))

    if (Role.query.filter_by(name='admin') in new_roles or Role.query.filter_by(
            name='moderator') in new_roles) and not is_admin:
        return redirect(url_for("users.users",
                                error="You can't modify admin or moderator users if you are not an admin!"))

    user.roles = new_roles
    db.session().commit()
    return redirect(url_for("users.users"))


@bp.route("/delete/<user_name>/")
@login_required(role='moderator')
def delete(user_name):
    user = User.query.filter_by(name=user_name).first()
    user_id = user.id

    # Check if 'admin' is in list of role names the user we are deleting has
    if 'admin' in list(map(lambda role: role.name, user.roles)):
        return redirect(url_for("users.users",
                                error="Admin accounts can not be removed!"))

    # Reset roles of user to guest in case same name re-registers
    user.roles = [Role.query.filter_by(name='guest').first()]
    db.session().commit()

    # Delete messages created by user
    Message.query.filter_by(account_id=user_id).delete()
    # Delete Messages in topics created by user
    for topic in Topic.query.filter_by(account_id=user_id).all():
        Message.query.filter_by(topic_id=topic.id).delete()
    # Delete topics created by user
    Topic.query.filter_by(account_id=user_id).delete()
    # Delete user
    User.query.filter_by(name=user_name).delete()

    db.session().commit()
    return redirect(url_for("users.users"))
