from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView, route
from flask_login import login_required

from app.forms.admin.project import ProjectForm
from app.models.Project import Project,SubProject,ImageCategory, ImageStore as Image


def get_project(project_id):
    return Project.query.filter_by(id=project_id).first_or_404()


class ProjectView(FlaskView):
    decorators = [login_required]

    def index(self):
        projects = Project.query.filter_by(type="combined").all()
        return render_template('admin/project/index.html', projects=projects)

    def create(self):
        form = ProjectForm()
        return render_template('admin/project/create.html', form=form)

    @route('/', methods=('POST',))
    def store(self):
        form = ProjectForm(request.form)
        if form.validate_on_submit():
            project = Project(title=form.title.data, description=form.description.data)
            project.save()
            flash("Project was created successfully", 'success')
            return redirect(url_for("admin.ProjectView:index"))
        else:
            return redirect(url_for("admin.ProjectView:create"))

    @route('/<project_id>', methods=('GET',))
    def show(self, project_id):
        project = get_project(project_id)
        return render_template('admin/project/show.html', project=project)

    @route('/<project_id>/edit', methods=('GET',))
    def edit(self, project_id):
        project = get_project(project_id)
        form = ProjectForm(title=project.title, description=project.description)
        return render_template('admin/project/edit.html', form=form, project_id=project_id)

    @route('/<project_id>/update', methods=('POST',))
    def update(self, project_id):
        project = get_project(project_id)
        form = ProjectForm(request.form)
        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.save()
            flash("Project was updated successfully", "success")
            return redirect(url_for("admin.ProjectView:index"))
        else:
            return redirect(request.url)

    @route('<project_id>/delete', methods=('POST',))
    def delete(self, project_id):
        project = get_project(project_id)
        project.delete()
        flash("Project was deleted successfully", 'success')
        return redirect(url_for('admin.ProjectView:index'))
