from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=36),
        EqualTo('confirm_password', message="Password must match.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired() ])
    submit = SubmitField('Submit')
