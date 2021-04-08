from flask import render_template, flash, redirect, abort, url_for
from flask_classful import FlaskView
from flask_login import login_required

from app.forms.admin.database.Category import CategoryForm
from app.models.Database import DatabaseCategory as Category


class DatabaseCategoryView(FlaskView):
    decorators = [login_required]

    def index(self):
        form = CategoryForm()
        projects = Category.query.all()
        return render_template('admin/database/category/index.html', projects=projects, form=form)

    def create(self):
        form = CategoryForm()
        return render_template('admin/database/category/create.html', form=form)

    def post(self, database_id):
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(description=form.description.data, title=form.title.data, database_id=database_id)
            category.create()
            flash('Category was created successfully', 'success')
            return redirect(url_for('admin.project_show', database_id=database_id))
        return abort(403)

    def delete(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        database_id = category.database_id
        category.delete()
        flash('Category was deleted successfully', 'success')
        return redirect(url_for('admin.DatabaseView:show', database_id=database_id))

    def edit(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        form = CategoryForm(description=category.description, title=category.title)
        return render_template('admin/database/category/edit.html', form=form)

    def update(self):
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category.query.filter_by(id=category_id).first_or_404()
            category.description = form.description.data
            category.title = form.title.data
            flash('Category was updated successfully', 'success')
            category.save()
            return redirect(url_for('admin.project_show', database_id=category.database_id))
        else:
            abort(403)

    def show(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        return render_template('admin/database/category/show.html', category=category)
