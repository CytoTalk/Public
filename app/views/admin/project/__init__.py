from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView, route
from flask_login import login_required
from sqlalchemy import and_

from app import db
from app.forms.admin.modify_access import AdditionForm

from app.forms.admin.modify_access import RemoveForm
from app.forms.admin.project import ProjectForm
from app.models.Project import Project, SubProject, ImageCategory, ImageStore as Image, allowed_user
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
            project = Project(title=form.title.data, description=form.description.data, status=form.status.data)
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
        form = ProjectForm(title=project.title, description=project.description, status=project.status)
        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.status = form.status.data
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
        project = get_project(project_id)
        form = AdditionForm()
        form.email.choices = [(user.id, user.email) for user in User.query.all()]

        if request.method == "POST":
            user = form.email.data
            allowed = allowed_user.insert().values(user_id=user, project_id=project_id)
            db.session.execute(allowed)
            db.session.commit()
            return redirect(url_for('admin.ProjectView:index'))
        return render_template("admin/project/add.html", form=form)

    '''remove users'''

    @route("<project_id>/remove", methods=('GET', 'POST',))
    def remove(self, project_id):
        project = get_project(project_id)
        form = RemoveForm()
        form.email.choices = [(user.id, user.email) for user in User.query.all()]

        if request.method == "POST":
            user = int(form.email.data)
            tuple_list = db.session.query(allowed_user).filter(user==user, project_id==project.id).delete()
            print(tuple_list)
            if tuple_list:
                db.session.commit()
            else:
                flash("The user wasn't part of the project", 'success')

            return redirect(url_for('admin.ProjectView:index'))
        return render_template("admin/project/remove.html", form=form)

    '''
    Possible use
    deleted_objects = User.__table__.delete().where(User.id.in_([1, 2, 3]))
    session.execute(deleted_objects)
    session.commit()
    '''
