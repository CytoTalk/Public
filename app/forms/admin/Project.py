from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired()])
    description = StringField('Project description', validators=[DataRequired()])
    submit = SubmitField('Submit')
