from pathlib import Path
from uuid import uuid4

from flask import render_template, flash, redirect, abort, url_for, current_app, send_from_directory
from flask.views import View
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.forms.admin.Image import ImageForm
from app.models.Image import Image


class ImagePost(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, category_id):
        form = ImageForm()
        if form.validate_on_submit():
            for image in form.images.data:
                name = str(Path(image.filename).stem)
                filename = str(uuid4())+'-'+ secure_filename(image.filename)
                path = str(Path('images', filename))
                image.save(Path(current_app.config['ASSETS_PATH'],path))
                image = Image(name=name, path=path, category_id=category_id)
                image.create()
            flash('Images were uploaded successfully', 'success')
            return redirect(url_for('admin.category_show', category_id=category_id))
        return abort(400, description="Make sure you have uploaded the correct files")


class ImageCreate(View):
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, category_id):
        form = ImageForm()
        return render_template('admin/image/create.html', form=form)


class ImageDelete(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        category_id = image.category_id
        image.delete()
        Path.unlink(Path(current_app.config['ASSETS_PATH'], image.path))
        flash('Image was deleted successfully', 'success')
        return redirect(url_for('admin.category_show', category_id=category_id))


class ImageEdit(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        form = ImageForm(description=image.description, title=image.title)
        return render_template('admin/image/edit.html', form=form)


class ImageUpdate(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, image_id):
        form = ImageForm()
        if form.validate_on_submit():
            image = Image.query.filter_by(id=image_id).first_or_404()
            image.title = form.title.data
            flash('Image was updated successfully', 'success')
            image.save(current_app.config['ASSETS_PATH'])
            return redirect(url_for('admin.project_show', category_id=image.category_id))
        else:
            abort(403)


class ImageShow(View):
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        return send_from_directory(str(Path(current_app.config['ASSETS_PATH'])),filename=image.path ,as_attachment=True)
