from flask import render_template, flash, redirect, abort, url_for
from flask_classful import FlaskView
from flask_login import login_required

from app.forms.admin.Project import ProjectForm
from app.models.Project import Project


class DatabaseView(FlaskView):
    decorators = [login_required]

    def index(self):
        form = ProjectForm()
        databases = Project.query.filter_by(type='single').all()
        return render_template('admin/database/index.html', databases=databases, form=form)

    def create(self):
        form = ProjectForm()
        return render_template('admin/database/create.html', form=form)

    def post(self):
        form = ProjectForm()
        if form.validate_on_submit():
            project = Project(description=form.description.data, title=form.title.data, type='single')
            project.create()
            flash('Project was created successfully', 'success')
            return redirect(url_for('admin.project_index'))
        return abort(403)

    def edit(self, database_id):
        project = Project.query.filter_by(id=database_id).first_or_404()
        form = ProjectForm(description=project.description, title=project.title)
        return render_template('admin/database/edit.html', form=form)

    def update(self, database_id):
        form = ProjectForm()
        if form.validate_on_submit():
            project = Project.query.filter_by(id=database_id).first_or_404()
            project.description = form.description.data
            project.title = form.title.data
            flash('Project was updated successfully', 'success')
            project.save()
            return redirect(url_for('admin.project_index'))
        else:
            abort(403)

    def show(self, database_id):
        project = Project.query.filter_by(id=database_id).first_or_404()
        return render_template('admin/database/show.html', project=project)

    def delete(self, database_id):
        project = Project.query.filter_by(id=database_id).first_or_404()
        project.delete()
        flash('Project was deleted successfully', 'success')
        return redirect(url_for('admin.project_index'))
