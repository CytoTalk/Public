from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

PROJECT_TYPES = [(1, 'Excel'), (2, 'Image')]


class ExcelCategoryForm(FlaskForm):
    title = StringField('Category Name', validators=[DataRequired()])
    description = StringField('Category description', validators=[DataRequired()])
    file = FileField('Excel File', validators=[FileAllowed(['xls', 'xlsx'], 'The file is not a valid excel file!')])
    submit = SubmitField('Submit')


class ImageCategoryForm(FlaskForm):
    title = StringField('Category Name', validators=[DataRequired()])
    description = StringField('Category description',  validators=[DataRequired()])
    submit = SubmitField('Submit')


