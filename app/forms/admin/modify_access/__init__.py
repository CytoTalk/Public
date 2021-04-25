from flask_wtf import FlaskForm
from wtforms import SelectField


class AdditionForm(FlaskForm):
    email = SelectField('email', choices=[])


class RemoveForm(FlaskForm):
    email = SelectField('email', choices=[])
