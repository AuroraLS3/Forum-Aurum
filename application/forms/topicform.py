from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, StringField


class TopicForm(FlaskForm):
    name = StringField("Title", validators=[validators.InputRequired()])
    message = TextAreaField("Message", [validators.InputRequired()])

    class Meta:
        csrf = False
