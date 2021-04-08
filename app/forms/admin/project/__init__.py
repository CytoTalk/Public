from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

PROJECT_TYPES = [(1, 'Excel'), (2, 'Image')]


class ProjectForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired()])
    description = StringField('Project description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SubProjectForm(FlaskForm):
    title = StringField('Sub Project Name', validators=[DataRequired()])
    description = StringField('Sub Project description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ExcelCategoryForm(FlaskForm):
    title = StringField('Category Name', validators=[DataRequired()])
    description = StringField('Category description', validators=[DataRequired()])
    excel = FileField('Excel File',
                      validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], 'The file is not a valid excel file!')])
    submit = SubmitField('Submit')


class ImageCategoryForm(FlaskForm):
    title = StringField('Category Name', validators=[DataRequired()])
    description = StringField('Category description', validators=[DataRequired()])
    submit = SubmitField('Submit')