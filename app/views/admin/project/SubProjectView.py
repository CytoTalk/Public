from pathlib import Path
from uuid import uuid4
import pandas as pd
from flask import request, flash, redirect, url_for, render_template, abort, current_app
from flask_classful import FlaskView, route
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db, csrf
from app.forms.admin.feature import FeatureForm
from app.forms.admin.project import ProjectForm, SubProjectForm, ExcelCategoryForm
from app.functions.store_excel import HandleExcel
from app.models.Excel import ExcelRecord, ExcelColumn
from app.models.Project import SubProject
from app.models.Feature import Feature as FeatureModel
from app.views.admin.project import create_user_permission, revoke_user_permission


def get_subproject(subproject_id):
    return SubProject.query.filter_by(id=subproject_id).first_or_404()


def get_feature(feature_id) -> FeatureModel:
    return FeatureModel.query.filter_by(id=feature_id).first_or_404()


def handle_excel_create(project_id, subproject_type):
    url = url_for('admin.SubProjectView:create', project_id=project_id, subproject_type=subproject_type)
    form = ExcelCategoryForm()
    if form.validate_on_submit():
        subproject = SubProject(title=form.title.data, description=form.description.data, type=subproject_type,
                                project_id=project_id)
        f = form.excel.data
        filename = str(uuid4()) + '-' + secure_filename(f.filename)
        path = str(Path('excel_files', filename))
        file_path = Path(current_app.config['ASSETS_PATH'], path)
        f.save(file_path)
        subproject.file_path = str(file_path)
        subproject.save()
        excel = HandleExcel(file_path, subproject)
        excel.store_columns()
        excel.store_records()
        flash("Data was stored successfully", "success")
        return redirect(url_for("admin.ProjectView:show", project_id=project_id))
    else:
        return render_template('admin/project/subproject/create.html', form=form, url=url)


def handle_image_create(project_id, subproject_type):
    url = url_for('admin.SubProjectView:create', subproject_type=subproject_type, project_id=project_id)
    form = SubProjectForm()

    if form.validate_on_submit():
        subproject = SubProject(
            description=form.description.data,
            title=form.title.data,
            project_id=project_id,
            type=subproject_type)
        subproject.create()
        flash('SubProject was created successfully', 'success')
        return redirect(url_for("admin.ProjectView:show", project_id=project_id))
    return render_template('admin/project/subproject/create.html', form=form, url=url)


def handle_feature_create(project_id, subproject_type):
    form = FeatureForm()
    if form.validate_on_submit():
        sub_project = SubProject(
            title=form.title.data,
            description=form.description.data,
            project_id=project_id,
            type=subproject_type,
            is_public=not form.status.data
        )
        sub_project.create()
        feature = FeatureModel(
            subproject_id=sub_project.id
        )
        feature.create()
        feature.make_db()
        flash("Feature Project was created successfully", "success")
        # return redirect(url_for("admin.FeatureView:index"))
        return redirect(url_for("admin.ProjectView:show", project_id=project_id))

    # return render_template('admin/feature/create.html', form=form)
    url = url_for('admin.SubProjectView:create', project_id=project_id, subproject_type=subproject_type)

    return render_template('admin/project/subproject/create.html', form=form, url=url)


def handle_excel_show(subproject, subproject_id):
    records = ExcelRecord.query.filter_by(subproject_id=subproject_id)
    df = pd.read_sql(records.statement, db.session.bind)
    df.drop(['CREATED_AT', 'UPDATED_AT', 'subproject_id', 'id'], axis=1, inplace=True)
    records = []
    for batch, df_batch in df.groupby('batch_id'):
        df_batch.drop(['batch_id', 'column_id'], axis=1, inplace=True)
        print(df_batch)
        records.append(df_batch.to_dict('list')['value'])
    return render_template('admin/project/subproject/show/excel.html', subproject=subproject, records=records)


class SubProjectView(FlaskView):
    decorators = [login_required]

    @route('/store/<project_id>/<subproject_type>', methods=('POST', 'GET',))
    def create(self, project_id, subproject_type):
        if subproject_type == 'excel':
            return handle_excel_create(project_id, subproject_type)

        elif subproject_type == 'image':
            return handle_image_create(project_id, subproject_type)

        elif subproject_type == 'feature':
            return handle_feature_create(project_id, subproject_type)
        else:
            abort(404)

    @route('subproject/<subproject_id>', methods=('GET',))
    def show(self, subproject_id):
        subproject = get_subproject(subproject_id)
        if subproject.type == 'excel':
            handle_excel_show(subproject, subproject_id)
        elif subproject.type == 'image':
            return render_template('admin/project/subproject/show/image.html', subproject=subproject)
        elif subproject.type == 'feature':
            feature = subproject.features[0]
            return render_template('admin/project/subproject/show/feature.html', feature=feature, subproject=subproject)
        abort(404)

    @route('/<subproject_id>/update', methods=('GET', 'POST',))
    def update(self, subproject_id):
        subproject = get_subproject(subproject_id)
        form = ProjectForm(title=subproject.title, description=subproject.description)
        if form.validate_on_submit():
            subproject.title = form.title.data
            subproject.description = form.description.data
            subproject.save()
            flash("Sub Project was updated successfully", "success")
            return redirect(url_for("admin.ProjectView:show", project_id=subproject.project_id))
        return render_template('admin/project/edit.html', form=form, subproject_id=subproject_id)

    @route('/update_column/<column_id>', methods=('POST',))
    @csrf.exempt
    def update_column(self, column_id):
        column = ExcelColumn.query.filter_by(id=column_id).first_or_404()
        column.title = request.form.get('title')
        column.description = request.form.get('description')
        column.save()
        flash('Column was updated successfully')
        return redirect(url_for('admin.SubProjectView:show', subproject_id=column.subproject_id))

    @route('<project_id>/subproject/<subproject_id>/delete', methods=('POST',))
    def delete(self, project_id, subproject_id):
        subproject = get_subproject(subproject_id)
        subproject.delete()
        flash("Sub Project was deleted successfully", 'success')
        return redirect(url_for('admin.ProjectView:show', project_id=project_id))

    '''
    Add users
    '''

    @route('<subproject_id>/add', methods=('GET', 'POST',))
    def add(self, subproject_id):
        subproject: SubProject = get_subproject(subproject_id)
        return create_user_permission(
            subproject,
            url_for('admin.SubProjectView:show', subproject_id=subproject_id))

    '''remove users'''

    @route("project/<subproject_id>/allowed_user/<user_id>/revoke", methods=('GET',))
    def remove(self, subproject_id, user_id):
        subproject = get_subproject(subproject_id)
        return revoke_user_permission(
            subproject, user_id,
            url_for('admin.SubProjectView:show', subproject_id=subproject_id))
