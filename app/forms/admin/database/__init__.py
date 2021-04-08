from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class DatabaseForm(FlaskForm):
    title = StringField('Database Name', validators=[DataRequired()])
    description = StringField('Database description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    title = StringField('Category Name', validators=[DataRequired()])
    description = StringField('Category description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ImageForm(FlaskForm):
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')
