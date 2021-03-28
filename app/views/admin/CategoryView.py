from flask import render_template, flash, redirect,  abort, url_for
from flask.views import View
from flask_login import login_required

from app.forms.admin.Category import CategoryForm
from app.models.Category import Category


class CategoryIndex(View):
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, category_id):
        form = CategoryForm()
        projects = Category.query.all()

        return render_template('admin/category/index.html', projects=projects, form=form)


class CategoryPost(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, project_id):
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(description=form.description.data, title=form.title.data, project_id=project_id)
            category.create()
            flash('Category was created successfully', 'success')
            return redirect(url_for('admin.project_show', project_id=project_id))
        return abort(403)


class CategoryCreate(View):
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, project_id):
        form = CategoryForm()
        return render_template('admin/category/create.html', form=form)


class CategoryDelete(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        project_id = category.project_id
        category.delete()
        flash('Category was deleted successfully', 'success')
        return redirect(url_for('admin.project_show', project_id=project_id))


class CategoryEdit(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        form = CategoryForm(description=category.description, title=category.title)
        return render_template('admin/category/edit.html', form=form)


class CategoryUpdate(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, category_id):
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category.query.filter_by(id=category_id).first_or_404()
            category.description = form.description.data
            category.title = form.title.data
            flash('Category was updated successfully', 'success')
            category.save()
            return redirect(url_for('admin.project_show', project_id=category.project_id))
        else:
            abort(403)


class CategoryShow(View):
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        return render_template('admin/category/show.html', category=category)
