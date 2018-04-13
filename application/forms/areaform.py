from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from application.models.role import Role


class AreaForm(FlaskForm):
    name = StringField("Name", validators=[validators.InputRequired()])
    description = TextAreaField("Description", [validators.InputRequired()])
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_pk=lambda a: a.id,
                            get_label=lambda a: a.name,
                            label="Who can view the area?")

    class Meta:
        csrf = False
