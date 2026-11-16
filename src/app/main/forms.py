from flask_wtf import FlaskForm
from wtforms import SubmitField


class RadiologistRequestForm(FlaskForm):
    submit = SubmitField("Request radiologist role")
