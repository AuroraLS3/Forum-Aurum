from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    name = StringField("Username", [validators.InputRequired(), validators.Length(max=100)])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(min=6)])

    class Meta:
        csrf = False
