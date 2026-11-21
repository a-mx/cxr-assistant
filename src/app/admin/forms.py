from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class RoleDecisionForm(FlaskForm):
    submit = SubmitField()

class FacilityForm(FlaskForm):
    name = StringField(
        "Facility name",
        validators=[
            DataRequired(),
            Length(min=1, max=64),
        ],
    )

    submit = SubmitField("Add facility")
