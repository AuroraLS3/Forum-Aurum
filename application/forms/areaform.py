from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, StringField, SelectMultipleField


class AreaForm(FlaskForm):
    name = StringField("Name", validators=[validators.InputRequired()])
    description = TextAreaField("Description", [validators.InputRequired()])
    roles = SelectMultipleField("Roles", choices=[], coerce=int, validators=[validators.InputRequired()])

    class Meta:
        csrf = False
