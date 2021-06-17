from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, MultipleFileField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired

PROJECT_TYPES = [(1, 'Excel'), (2, 'Image')]
PERMISSION_CHOICES = [('CREATE', 'CREATE'), ('READ', 'READ'), ('UPDATE', 'UPDATE'), ('DELETE', 'DELETE')]


class ProjectForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired()])
    description = StringField('Project description', validators=[DataRequired()])

    '''Make the change to the form as well'''
    status = BooleanField("private")
    submit = SubmitField('Submit')


class SubProjectForm(FlaskForm):
    title = StringField('Sub Project Name', validators=[DataRequired()])
    description = StringField('Sub Project description', validators=[DataRequired()])
    status = BooleanField("private")
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


class ImageForm(FlaskForm):
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')


class ModelPermissionForm(FlaskForm):
    email = SelectField('email', choices=[], validators=[DataRequired()])
    permission = SelectMultipleField('Permission (Select all that apply)', choices=PERMISSION_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Submit')
