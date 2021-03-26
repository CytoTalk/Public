from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo,Length

from app.forms import BaseForm


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=36),
        EqualTo('confirm_password', message="Password must match.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired() ])
    submit = SubmitField('Register')
