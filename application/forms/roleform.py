from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from application.models.role import Role


class RoleForm(FlaskForm):
    roles = QuerySelectMultipleField(
        # query factory gets all roles that are not anyone, moderator or admin
        query_factory=lambda: Role.query.filter(
            and_(Role.name != 'anyone', Role.name != 'moderator', Role.name != 'admin')
        ).all(),
        get_pk=lambda a: a.id,
        get_label=lambda a: a.name,
        label="",
        validators=[validators.InputRequired()])


class RoleFormAdmin(FlaskForm):
    # query factory gets all roles that are not anyone
    roles = QuerySelectMultipleField(query_factory=lambda: Role.query.filter(Role.name != 'anyone').all(),
                                     get_pk=lambda a: a.id,
                                     get_label=lambda a: a.name,
                                     label="",
                                     validators=[validators.InputRequired()])

    class Meta:
        csrf = False
