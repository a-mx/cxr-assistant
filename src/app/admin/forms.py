from flask_wtf import FlaskForm
from wtforms import SubmitField


class RoleDecisionForm(FlaskForm):
    submit = SubmitField()
