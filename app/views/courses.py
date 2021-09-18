from pathlib import Path
from flask import request, render_template
from flask_classful import FlaskView, route
from app.models.Course import Course


class CourseView(FlaskView):
    """
    This is where editing begins
    """

    @route('/', methods=('GET',))
    def index(self):

        courses = Course.query.all()

        return render_template('front/course/index.html', courses=courses)

    @route('/<course_slug>', methods=('GET',))
    def show(self, course_slug):
        course = Course.query.filter_by(slug=course_slug).first_or_404()
        return render_template(
            'front/course/show.html', course=course)

