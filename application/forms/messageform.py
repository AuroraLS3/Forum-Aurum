from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators


class MessageForm(FlaskForm):
    content = TextAreaField("Message", [validators.InputRequired()])

    class Meta:
        csrf = False
