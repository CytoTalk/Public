from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

PROJECT_TYPES = [(1, 'Excel'), (2, 'Image')]


class ProjectAlLForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired()])
    description = StringField('Project description', validators=[DataRequired()])
    submit = SubmitField('Submit')


