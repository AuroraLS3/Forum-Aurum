from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class RegisterForm(FlaskForm):
    name = StringField("Username", [validators.InputRequired(), validators.Length(max=100)])
    password = PasswordField("Password", [validators.Length(min=6, max=130),
                                          validators.EqualTo('password_again', message='Passwords must match!')])
    password_again = PasswordField("Password Again")

    class Meta:
        csrf = False
