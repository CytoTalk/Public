from cloudinary.uploader import upload, destroy
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_classful import FlaskView, route
from flask_login import login_required
from slugify import slugify
from app.forms.admin.course import CourseForm
from app.models.Course import Course, CourseImage


def get_course(course_id: int) -> Course:
    return Course.query.get(course_id)


def unique_slug(text) -> str:
    slug = slugify(text)
    course = Course.query.filter_by(slug=slug).all()
    if not course:
        return slug
    return slug + f"-{len(course)}"


class CourseView(FlaskView):
    decorators = [login_required]

    def index(self):
        courses = Course.query.all()
        return render_template('admin/course/index.html', courses=courses)

    @route('/create', methods=['GET', 'POST'])
    def create(self):
        form = CourseForm()
        if form.validate_on_submit():
            course = Course.query.filter_by(title=form.title.data).first()
            if course:
                flash("A course with the title already exist", 'error')
                return redirect(request.url)

            course = Course(
                long_description=form.long_description.data,
                short_description=form.short_description.data,
                title=form.title.data,
                price=form.price.data,
                slug=unique_slug(form.title.data)
            )
            course.save()

            try:
                main_picture_upload = upload(form.main_picture.data)
                CourseImage(
                    public_id=main_picture_upload['public_id'],
                    url=main_picture_upload['secure_url'],
                    is_main_picture=True,
                    course_id=course.id
                ).save()
            except Exception as exception:
                flash(str(exception), 'error')
                return redirect(request.url)

            if len(form.other_images.data):
                image_bag = []

                for image in form.other_images.data:
                    try:
                        image_bag.append(upload(image))
                    except Exception as exception:
                        flash(str(exception), 'error')
                if image_bag:
                    for image in image_bag:
                        CourseImage(
                            public_id=image['public_id'],
                            url=image['secure_url'],
                            is_main_picture=False,
                            course_id=course.id
                        ).save()
            flash("Course was created successfully", 'success')
            return redirect(url_for('admin.CourseView:index'))
        else:
            return render_template('admin/course/create.html', form=form)

    @route('/<course_id>/update', methods=('GET', 'POST',))
    def update(self, course_id):
        course = get_course(course_id)
        form = CourseForm(long_description=course.long_description,
                          short_description=course.short_description, price=course.price,
                          title=course.title)
        if request.method == 'POST':
            course.long_description = form.long_description.data
            course.short_description = form.short_description.data
            course.title = form.title.data
            course.price = form.price.data
            course.slug = unique_slug(form.title.data)
            course.save()
            images_to_delete = request.form.getlist('images_to_delete')
            if images_to_delete:
                for image in images_to_delete:
                    destroy(image)
                    result = CourseImage.query.filter_by(public_id=image).first()
                    if result:
                        result.delete()
            if form.main_picture.data:

                try:
                    main_picture_upload = upload(form.main_picture.data)

                    query = CourseImage.query.filter_by(is_main_picture=True, course_id=course.id).first()
                    query.public_id = main_picture_upload['public_id']
                    query.url = main_picture_upload['secure_url']
                    query.save()

                except Exception as exception:
                    flash(str(exception), 'error')
            if len(form.other_images.data):
                image_bag = []

                for image in form.other_images.data:
                    try:
                        image_bag.append(upload(image))
                    except Exception as exception:
                        flash(str(exception), 'error')
                if image_bag:
                    for image in image_bag:
                        CourseImage(
                            public_id=image['public_id'],
                            url=image['secure_url'],
                            is_main_picture=False,
                            course_id=course.id
                        ).save()
            flash("Course was updated successfully", "success")

            return redirect(url_for("admin.CourseView:index"))
        return render_template('admin/course/edit.html', form=form, course=course)

    @route('/<course_id>', methods=('GET',))
    def show(self, course_id):
        course = get_course(course_id)
        return render_template('admin/course/show.html', course=course)

    @route('<course_id>/delete', methods=('POST',))
    def delete(self, course_id):
        course = get_course(course_id)
        course.delete()
        flash("Course was deleted successfully", 'success')
        return redirect(url_for('admin.CourseView:index'))
