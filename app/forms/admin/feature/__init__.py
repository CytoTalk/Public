from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, MultipleFileField, BooleanField
from wtforms.validators import DataRequired

from app.models.Feature import DATA_TYPES_MAPPER


class FeatureForm(FlaskForm):
    title = StringField('Feature Project Name', validators=[DataRequired()])
    description = StringField('Feature Project description', validators=[DataRequired()])

    '''Make the change to the form as well'''
    status = BooleanField("private")
    submit = SubmitField('Submit')


class ColumnForm(FlaskForm, ):
    disabled = 'false'
    name = StringField('Column Name', validators=[DataRequired()])
    description = StringField('Column description', validators=[DataRequired()])
    data_type = SelectField('Data Type', choices=DATA_TYPES_MAPPER.keys(), validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, disabled=False, **kw):
        super(ColumnForm, self).__init__(**kw)
        if disabled:
            self.data_type.render_kw = {"hidden": "hidden"}
