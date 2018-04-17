from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators


class MessageForm(FlaskForm):
    message = TextAreaField("Message", [validators.InputRequired(), validators.Length(max=1000)])

    class Meta:
        csrf = False
