from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

from src.app.models import Patient


class PatientForm(FlaskForm):
    name = StringField(
        "First name",
        validators=[
            DataRequired(),
            Length(min=1, max=64),
        ],
    )

    surname = StringField(
        "Surname",
        validators=[
            DataRequired(),
            Length(min=1, max=64),
        ],
    )

    pesel = StringField(
        "PESEL",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{11}$",
                message="PESEL must contain exactly 11 digits.",
            ),
        ],
    )

    submit = SubmitField("Add patient")

    def validate_pesel(self, field):
        pesel = field.data.strip()

        if Patient.query.filter_by(pesel=pesel).first():
            raise ValidationError(
                "A patient with this PESEL already exists."
            )