from flask import request, flash, redirect, url_for, render_template, abort
from flask_classful import FlaskView, route
from flask_login import login_required

from app.forms.admin.project import ProjectForm, ProjectPermissionForm
from app.models.Project import Project, AllowedUser
from app.models.User import User


def get_project(project_id):
    return Project.query.filter_by(id=project_id).first_or_404()


class ProjectView(FlaskView):
    decorators = [login_required]

    def index(self):
        projects = Project.query.all()
        return render_template('admin/project/index.html', projects=projects)

    @route('/create', methods=('POST', 'GET',))
    def create(self):
        form = ProjectForm()
        if form.validate_on_submit():
            project = Project(title=form.title.data, description=form.description.data, is_public=not form.status.data)
            project.save()
            flash("Project was created successfully", 'success')
            return redirect(url_for("admin.ProjectView:index"))
        return render_template('admin/project/create.html', form=form)

    @route('/<project_id>', methods=('GET',))
    def show(self, project_id):
        project = get_project(project_id)
        return render_template('admin/project/show.html', project=project)

    @route('/<project_id>/update', methods=('GET', 'POST',))
    def update(self, project_id):
        project = get_project(project_id)
        form = ProjectForm(title=project.title, description=project.description, is_public=project.is_public)
        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.is_public = not form.status.data
            project.save()
            flash("Project was updated successfully", "success")
            return redirect(url_for("admin.ProjectView:index"))
        return render_template('admin/project/edit.html', form=form, project_id=project_id)

    @route('<project_id>/delete', methods=('POST',))
    def delete(self, project_id):
        project = get_project(project_id)
        project.delete()
        flash("Project was deleted successfully", 'success')
        return redirect(url_for('admin.ProjectView:index'))

    '''
    Add users
    '''

    @route('<project_id>/add', methods=('GET', 'POST',))
    def add(self, project_id):
        form: ProjectPermissionForm = ProjectPermissionForm()
        project: Project = get_project(project_id)
        form.email.choices = [(user.id, user.email) for user in User.query.all() if
                              user not in [permitted.user for permitted in project.allowed_users]]

        if form.validate_on_submit():
            user_id = form.email.data
            user_exists = AllowedUser.query.filter_by(user_id=user_id, project_id=project_id).first()
            if user_exists:
                flash("User already permitted to view this project!", 'error')
                return redirect(request.url)
            allowed = AllowedUser(user_id=form.email.data, project_id=project_id)
            allowed.save()
            flash("User has been permitted to view the project", "success")
            return redirect(url_for('admin.ProjectView:show', project_id=project_id))
        return render_template("admin/project/add.html", form=form)

    '''remove users'''

    @route("project/<project_id>/allowed_user/<user_id>/revoke", methods=('GET',))
    def remove(self, project_id, user_id):
        user_permitted: AllowedUser = AllowedUser.query.filter_by(user_id=user_id, project_id=project_id).first()
        if user_permitted:
            user_permitted.delete()
            flash("User permission to the project was revoked", "success")
        else:
            flash("User is not enrolled to this project")
        return redirect(url_for('admin.ProjectView:show', project_id=project_id))
