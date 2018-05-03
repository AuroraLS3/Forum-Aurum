import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import db
from application.forms.loginform import LoginForm
from application.forms.registerform import RegisterForm
from application.models.role import Role
from application.models.user import User

bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')


@bp.route("/register/")
def register_page():
    return render_template("auth/register.html", form=RegisterForm())


@bp.route("/register/", methods=["POST"])
def register():
    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/register.html", form=form)

    name = form.name.data

    user = User.query.filter_by(name=name).first()
    if (user is not None):
        return render_template("auth/register.html", form=form, error="User Already Exists!")

    password = form.password.data.encode()

    hashpw = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
    registeringUser = User(name, hashpw)
    if User.find_user_count() == 0:
        registeringUser.roles.extend(Role.query.all())
    else:
        registeringUser.roles.append(Role.query.filter_by(name='guest').first())

    db.session().add(registeringUser)
    db.session().commit()

    user = User.query.filter_by(name=name).first()
    login_user(user)
    return redirect(url_for("forum.forum_main"))


@bp.route("/login/")
def login_page():
    return render_template("auth/login.html", form=LoginForm())


@bp.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("forum.forum_main"))


@bp.route("/login/", methods=["POST"])
def login():
    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/login.html", form=form)

    name = form.name.data

    user = User.query.filter_by(name=name).first()

    if user is None:
        return render_template("auth/login.html", form=form, error="User doesn't exist")

    password = form.password.data.encode()
    correctPass = bcrypt.checkpw(password, user.password.encode())

    if not correctPass:
        return render_template("auth/login.html", form=form, error="Incorrect Password")

    login_user(user)
    return redirect(url_for("forum.forum_main"))
