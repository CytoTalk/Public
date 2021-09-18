from flask import Blueprint

from app.views.courses import CourseView

course = Blueprint('course', __name__,)
CourseView.register(course, trailing_slash=False)
