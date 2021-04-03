from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView, route
from flask_login import login_required

from app.forms.admin.project_all.ProjectAll import ProjectAlLForm
from app.models.Category import Category
from app.models.Project import Project


def get_project(project_id):
    return Project.query.filter_by(id=project_id).first_or_404()


class AllProjectView(FlaskView):
    decorators = [login_required]

    def index(self):
        projects = Project.query.filter_by(type="combined").all()
        return render_template('admin/project_all/index.html', projects=projects)

    def create(self):
        form = ProjectAlLForm()
        return render_template('admin/project_all/create.html', form=form)

    @route('/', methods=('POST',))
    def store(self):
        form = ProjectAlLForm(request.form)
        if form.validate_on_submit():
            project = Project(title=form.title.data, description=form.description.data, type='combined')
            project.save()
            flash("Project was created successfully", 'success')
            return redirect(url_for("admin.AllProjectView:index"))
        else:
            return redirect(url_for("admin.AllProjectView:create"))

    @route('/<project_id>', methods=('GET',))
    def show(self, project_id):
        project = get_project(project_id)
        categories = Category.query.filter_by(project_id=project_id).all()
        return render_template('admin/project_all/show.html', project=project, categories=categories)

    @route('/<project_id>/edit', methods=('GET',))
    def edit(self, project_id):
        project = get_project(project_id)
        form = ProjectAlLForm(title=project.title, description=project.description)
        return render_template('admin/project_all/edit.html', form=form, project_id=project_id)

    @route('/<project_id>/update', methods=('POST',))
    def update(self, project_id):
        project = get_project(project_id)
        form = ProjectAlLForm(request.form)
        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.save()
            flash("Project was updated successfully", "success")
            return redirect(url_for("admin.AllProjectView:index"))
        else:
            return redirect(request.url)

    @route('<project_id>/delete', methods=('POST',))
    def delete(self, project_id):
        project = get_project(project_id)
        project.delete()
        flash("Project was deleted successfully", 'success')
        return redirect(url_for('admin.AllProjectView:index'))