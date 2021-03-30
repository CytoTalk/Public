from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

PROJECT_TYPES = [(1, 'Excel'), (2, 'Image')]


class ProjectAlLForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired()])
    description = StringField('Project description', validators=[DataRequired()])
    # type = SelectField("Project Type", choices=PROJECT_TYPES, validators=[DataRequired()])
    submit = SubmitField('Submit')
