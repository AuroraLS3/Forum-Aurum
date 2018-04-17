from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, StringField


class TopicForm(FlaskForm):
    name = StringField("Title", validators=[validators.InputRequired(), validators.Length(max=100)])
    message = TextAreaField("Message", [validators.InputRequired(), validators.Length(max=1000)])

    class Meta:
        csrf = False
