from flask import render_template, flash, redirect, abort, url_for
from flask_classful import FlaskView, route
from flask_login import login_required

from app.forms.admin.database import CategoryForm
from app.models.Database import DatabaseCategory as Category


class DatabaseCategoryView(FlaskView):
    decorators = [login_required]

    @route('/<database_id>/create', methods=('POST', 'GET',))
    def create(self, database_id):
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(description=form.description.data, title=form.title.data, database_id=database_id)
            category.create()
            flash('Category was created successfully', 'success')
            return redirect(url_for('admin.DatabaseView:show', database_id=database_id))
        return render_template('admin/database/category/create.html', form=form)

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
            return redirect(url_for('admin.DatabaseView:show', database_id=category.database_id))
        return render_template('admin/database/category/edit.html', form=form)

    def show(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        return render_template('admin/database/category/show.html', category=category)

    @route('/<category_id>/delete', methods=('POST',))
    def delete(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        database_id = category.database_id
        category.delete()
        flash('Category was deleted successfully', 'success')
        return redirect(url_for('admin.DatabaseView:show', database_id=database_id))
