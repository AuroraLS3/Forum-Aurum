from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired()])
    password = PasswordField("Password", [validators.Length(min=6), validators.EqualTo('password_again')])
    password_again = PasswordField("Password Again")

    class Meta:
        csrf = False
