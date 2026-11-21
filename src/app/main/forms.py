from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import (
    DataRequired,
)


class RadiologistRequestForm(FlaskForm):
    facility_id = SelectField(
        "Facility",
        coerce=int,
        validators=[DataRequired()],
    )

    submit = SubmitField("Request radiologist role")
