from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
