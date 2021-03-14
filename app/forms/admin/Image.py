from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    name = StringField('Image Name', validators=[DataRequired()])
    path = FileField('Category description',  validators=[DataRequired()])
    submit = SubmitField('Submit')
