from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class PostForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    name = StringField('Name', validators=[Required()])
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Submit')