from flask import render_template, flash, redirect, abort, url_for
from flask_classful import FlaskView, route
from flask_login import login_required

from app.forms.admin.database import DatabaseForm
from app.models.Database import Database


class DatabaseView(FlaskView):
    decorators = [login_required]

    def index(self):
        databases = Database.query.all()
        return render_template('admin/database/index.html', databases=databases)

    @route('/create', methods=('GET', 'POST',))
    def create(self):
        form = DatabaseForm()
        if form.validate_on_submit():
            database = Database(description=form.description.data, title=form.title.data)
            database.create()
            flash('Database was created successfully', 'success')
            return redirect(url_for('admin.DatabaseView:index'))
        return render_template('admin/database/create.html', form=form)


    @route('/<database_id>/update', methods=('POST','GET',))
    def update(self, database_id):
        database = Database.query.filter_by(id=database_id).first_or_404()
        form = DatabaseForm(description=database.description, title=database.title)
        if form.validate_on_submit():
            database = Database.query.filter_by(id=database_id).first_or_404()
            database.description = form.description.data
            database.title = form.title.data
            flash('Database was updated successfully', 'success')
            database.save()
            return redirect(url_for('admin.DatabaseView:index'))
        return render_template('admin/database/edit.html', form=form)

    def show(self, database_id):
        database = Database.query.filter_by(id=database_id).first_or_404()
        return render_template('admin/database/show.html', database=database)

    @route('/<database_id>/delete', methods=('POST',))
    def delete(self, database_id):
        database = Database.query.filter_by(id=database_id).first_or_404()
        database.delete()
        flash('Database was deleted successfully', 'success')
        return redirect(url_for('admin.DatabaseView:index'))
