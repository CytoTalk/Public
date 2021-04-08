from flask import render_template, flash, redirect, abort, url_for
from flask_classful import FlaskView
from flask_login import login_required

from app.forms.admin.database import DatabaseForm
from app.models.Database import Database


class DatabaseView(FlaskView):
    decorators = [login_required]

    def index(self):
        databases = Database.query.filter_by(type='single').all()
        return render_template('admin/database/index.html', databases=databases)

    def create(self):
        form = DatabaseForm()
        return render_template('admin/database/create.html', form=form)

    def post(self):
        form = DatabaseForm()
        if form.validate_on_submit():
            project = Database(description=form.description.data, title=form.title.data, type='single')
            project.create()
            flash('Database was created successfully', 'success')
            return redirect(url_for('admin.project_index'))
        return abort(403)

    def edit(self, database_id):
        project = Database.query.filter_by(id=database_id).first_or_404()
        form = DatabaseForm(description=project.description, title=project.title)
        return render_template('admin/database/edit.html', form=form)

    def update(self, database_id):
        form = DatabaseForm()
        if form.validate_on_submit():
            project = Database.query.filter_by(id=database_id).first_or_404()
            project.description = form.description.data
            project.title = form.title.data
            flash('Database was updated successfully', 'success')
            project.save()
            return redirect(url_for('admin.project_index'))
        else:
            abort(403)

    def show(self, database_id):
        project = Database.query.filter_by(id=database_id).first_or_404()
        return render_template('admin/database/show.html', project=project)

    def delete(self, database_id):
        project = Database.query.filter_by(id=database_id).first_or_404()
        project.delete()
        flash('Database was deleted successfully', 'success')
        return redirect(url_for('admin.project_index'))
