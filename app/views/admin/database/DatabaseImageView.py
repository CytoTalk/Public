from pathlib import Path
from uuid import uuid4

from flask import render_template, flash, redirect, abort, url_for, current_app, send_from_directory
from flask_classful import FlaskView, route
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.forms.admin.database import ImageForm
from app.models.Database import Image


class DatabaseImageView(FlaskView):
    decorators = [login_required]

    @route('/<category_id>/update', methods=('POST', 'GET',))
    def create(self, category_id):
        form = ImageForm()
        if form.validate_on_submit():
            for image in form.images.data:
                name = str(Path(image.filename).stem)
                filename = str(uuid4()) + '-' + secure_filename(image.filename)
                path = str(Path('images', filename))
                image.save(Path(current_app.config['ASSETS_PATH'], path))
                image = Image(name=name, path=path, category_id=category_id)
                image.create()
            flash('Images were uploaded successfully', 'success')
            return redirect(url_for('admin.DatabaseCategoryView:show', category_id=category_id))
        return render_template('admin/image/create.html', form=form)

    @route('/<image_id>/update', methods=('POST', 'GET',))
    def update(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        form = ImageForm(description=image.description, title=image.title)
        if form.validate_on_submit():
            image = Image.query.filter_by(id=image_id).first_or_404()
            image.title = form.title.data
            flash('Image was updated successfully', 'success')
            image.save(current_app.config['ASSETS_PATH'])
            return redirect(url_for('admin.DatabaseCategoryView:show', category_id=image.category_id))
        else:
            return render_template('admin/image/edit.html', form=form)

    def show(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        return send_from_directory(str(Path(current_app.config['ASSETS_PATH'])), filename=image.path,
                                   as_attachment=True)


    @route('/<image_id>/delete', methods=('POST', 'GET',))
    def delete(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        category_id = image.category_id
        image.delete()
        Path.unlink(Path(current_app.config['ASSETS_PATH'], image.path))
        flash('Image was deleted successfully', 'success')
        return redirect(url_for('admin.DatabaseCategoryView:show', category_id=category_id))