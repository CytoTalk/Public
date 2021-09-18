from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired


class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    price = IntegerField("Price (USD)")
    short_description = StringField('Short Description', validators=[DataRequired()])
    long_description = TextAreaField('Long Description', validators=[DataRequired()])
    main_picture = FileField('Main Image',
                             validators=[
                                 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'),
                             ])
    other_images = MultipleFileField('Other Images', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')
