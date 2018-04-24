from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from application.models.role import Role


class RoleForm(FlaskForm):
    roles = QuerySelectMultipleField(query_factory=lambda: Role.query.all(),
                                     get_pk=lambda a: a.id,
                                     get_label=lambda a: a.name,
                                     label="",
                                     validators=[validators.InputRequired()])

    class Meta:
        csrf = False
