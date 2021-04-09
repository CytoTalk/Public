from flask import render_template, flash, redirect, abort, url_for
from flask_classful import FlaskView, route
from flask_login import login_required

from app.forms.admin.project import ImageCategoryForm as CategoryForm
from app.models.Project import ImageCategory as Category


class ProjectImageCategoryView(FlaskView):
    decorators = [login_required]

    @route('/<subproject_id>/create', methods=('POST', 'GET',))
    def create(self, subproject_id):
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(description=form.description.data, title=form.title.data, subproject_id=subproject_id)
            category.create()
            flash('Category was created successfully', 'success')
            return redirect(url_for('admin.SubProjectView:show', subproject_id=subproject_id))
        return render_template('admin/project/subproject/category/create.html', form=form)

    @route('/<category_id>/update', methods=('POST', 'GET',))
    def update(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        form = CategoryForm(description=category.description, title=category.title)
        if form.validate_on_submit():
            category = Category.query.filter_by(id=category_id).first_or_404()
            category.description = form.description.data
            category.title = form.title.data
            flash('Category was updated successfully', 'success')
            category.save()
            return redirect(url_for('admin.SubProjectView:show', subproject_id=category.subproject_id))
        return render_template('admin/project/subproject/category/edit.html', form=form)

    def show(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        return render_template('admin/project/subproject/category/show.html', category=category)

    @route('/<category_id>/delete', methods=('POST',))
    def delete(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        subproject_id = category.subproject_id
        category.delete()
        flash('Category was deleted successfully', 'success')
        return redirect(url_for('admin.SubProjectView:show', subproject_id=subproject_id))
