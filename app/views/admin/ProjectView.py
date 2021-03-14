from flask import render_template, flash, redirect, request, abort, url_for
from flask.views import MethodView, View

from app.forms.admin.Project import ProjectForm
from app.models.Project import Project


class ProjectIndex(View):
    methods = ['GET']

    def dispatch_request(self):
        form = ProjectForm()
        projects = Project.query.all()

        return render_template('admin/project/index.html', projects=projects, form=form)


class ProjectPost(View):
    methods = ['POST']

    def dispatch_request(self):
        form = ProjectForm()
        if form.validate_on_submit():
            project = Project(description=form.description.data, title=form.title.data)
            project.create()
            flash('Project was created successfully', 'success')
            return redirect(url_for('admin.project_index'))
        return abort(403)


class ProjectCreate(View):
    methods = ['GET']

    def dispatch_request(self):
        form = ProjectForm()
        return render_template('admin/project/create.html', form=form)


class ProjectDelete(View):
    methods = ['POST']

    def dispatch_request(self,project_id):
        project = Project.query.filter_by(id=project_id).first_or_404()
        project.delete()
        flash('Project was deleted successfully', 'success')
        return redirect(url_for('admin.project_index'))


class ProjectEdit(View):
    methods = ['POST']

    def dispatch_request(self, project_id):
        project = Project.query.filter_by(id=project_id).first_or_404()
        form = ProjectForm(description=project.description, title=project.title)
        return render_template('admin/project/edit.html', form=form)


class ProjectUpdate(View):
    methods = ['POST']

    def dispatch_request(self, project_id):
        form = ProjectForm()
        if form.validate_on_submit():
            project = Project.query.filter_by(id=project_id).first_or_404()
            project.description = form.description.data
            project.title = form.title.data
            flash('Project was updated successfully', 'success')
            project.save()
            return redirect(url_for('admin.project_index'))
        else:
            abort(403)


class ProjectShow(View):
    methods = ['GET']

    def dispatch_request(self, project_id):
        project = Project.query.filter_by(id=project_id).first_or_404()
        return render_template('admin/project/show.html', project=project)
