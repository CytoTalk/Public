from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,BooleanField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email/Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    is_active = BooleanField("Is active?")
    submit = SubmitField('Submit')

    # password = PasswordField('', validators=[DataRequired()])
