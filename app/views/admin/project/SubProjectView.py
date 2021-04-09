from pathlib import Path
from uuid import uuid4
import pandas as pd
from flask import request, flash, redirect, url_for, render_template, abort, current_app, jsonify
from flask_classful import FlaskView, route
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db, csrf
from app.forms.admin.project import ProjectForm, SubProjectForm, ExcelCategoryForm, ImageCategoryForm
from app.functions.store_excel import HandleExcel
from app.models.Excel import ExcelRecord, ExcelColumn
from app.models.Project import Project, SubProject


def get_subproject(subproject_id):
    return SubProject.query.filter_by(id=subproject_id).first_or_404()


class SubProjectView(FlaskView):
    decorators = [login_required]

    @route('/store/<project_id>/<subproject_type>', methods=('POST', 'GET',))
    def create(self, project_id, subproject_type):
        form, url = None, None
        if subproject_type == 'excel':
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

        elif subproject_type == 'image':
            url = url_for('admin.SubProjectView:create', subproject_type='image', project_id=project_id)
            form = SubProjectForm()

            if form.validate_on_submit():
                subproject = SubProject(description=form.description.data, title=form.title.data, project_id=project_id,
                                        type='image')
                subproject.create()
                flash('SubProject was created successfully', 'success')
                return redirect(url_for("admin.ProjectView:show", project_id=project_id))
            else:
                return render_template('admin/project/subproject/create.html', form=form, url=url)
        else:
            abort(404)

    @route('subproject/<subproject_id>', methods=('GET',))
    def show(self, subproject_id):
        subproject = get_subproject(subproject_id)
        if subproject.type == 'excel':
            records = ExcelRecord.query.filter_by(subproject_id=subproject_id)
            df = pd.read_sql(records.statement, db.session.bind)
            df.drop(['CREATED_AT', 'UPDATED_AT', 'subproject_id', 'id'], axis=1, inplace=True)
            records = []
            for batch, df_batch in df.groupby('batch_id'):
                df_batch.drop(['batch_id', 'column_id'], axis=1, inplace=True)
                print(df_batch)
                records.append(df_batch.to_dict('list')['value'])
            return render_template('admin/project/subproject/show/excel.html', subproject=subproject, records=records)
        else:
            return render_template('admin/project/subproject/show/image.html', subproject=subproject)

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
