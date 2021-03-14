from flask_wtf import FlaskForm
from flask_wtf.file import  FileAllowed
from wtforms import SubmitField, MultipleFileField


class ImageForm(FlaskForm):
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')
