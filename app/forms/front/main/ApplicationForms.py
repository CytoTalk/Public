from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, MultipleFileField, BooleanField,IntegerField
from wtforms.validators import DataRequired

excel = FileField('Excel File',
                  validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], 'The file is not a valid excel file!')])


class ExcelToListForm(FlaskForm):
    file = FileField('Excel File',
                     validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], 'The file is not a valid excel file!')])
    key_column = IntegerField("Key column", validators=[DataRequired()])
    target_column = IntegerField("Target column", validators=[DataRequired()])
    delimiter = StringField("Delimiter", validators=[DataRequired()])
    submit = SubmitField("Submit")
