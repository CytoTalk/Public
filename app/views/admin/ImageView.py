from flask import render_template, flash, redirect,  abort, url_for
from flask.views import View

from app.forms.admin.Image import ImageForm
from app.models.Image import Image


class ImageIndex(View):
    methods = ['GET']

    def dispatch_request(self, category_id):
        form = ImageForm()
        images = Image.query.all()

        return render_template('admin/category/index.html', projects=projects, form=form)


class ImagePost(View):
    methods = ['POST']

    def dispatch_request(self, category_id):
        form = ImageForm()
        if form.validate_on_submit():
            image = Image(description=form.description.data, title=form.title.data, category_id=category_id)
            image.create()
            flash('Image was created successfully', 'success')
            return redirect(url_for('admin.project_show', category_id=category_id))
        return abort(403)


class ImageCreate(View):
    methods = ['GET']

    def dispatch_request(self, category_id):
        form = ImageForm()
        return render_template('admin/image/create.html', form=form)


class ImageDelete(View):
    methods = ['POST']

    def dispatch_request(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        category_id = image.category_id
        image.delete()
        flash('Image was deleted successfully', 'success')
        return redirect(url_for('admin.project_show', category_id=category_id))


class ImageEdit(View):
    methods = ['POST']

    def dispatch_request(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        form = ImageForm(description=image.description, title=image.title)
        return render_template('admin/image/edit.html', form=form)


class ImageUpdate(View):
    methods = ['POST']

    def dispatch_request(self, image_id):
        form = ImageForm()
        if form.validate_on_submit():
            image = Image.query.filter_by(id=image_id).first_or_404()
            image.description = form.description.data
            image.title = form.title.data
            flash('Image was updated successfully', 'success')
            image.save()
            return redirect(url_for('admin.project_show', category_id=image.category_id))
        else:
            abort(403)


class ImageShow(View):
    methods = ['GET']

    def dispatch_request(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        return render_template('admin/image/show.html', image=image)
