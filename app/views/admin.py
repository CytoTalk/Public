from flask_login import login_required
from app.admin import admin
from flask import render_template, request, redirect, flash
from app.forms.admin.Project import ProjectForm
from app.models.Project import Project


@admin.route('/dashboard', methods=('GET',))
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin.route('/project', methods=('POST', 'GET'))
def create_project():
    form = ProjectForm()
    projects = Project.query.all()
    import pdb;pdb.set_trace()
    if form.validate_on_submit():
        project = Project(description=form.description.data, title=form.title.data)
        project.create()
        flash('Project was created successfully', 'success')
        return redirect(request.url)
    return render_template('admin/project/create.html', form=form)
