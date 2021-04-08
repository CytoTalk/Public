from pathlib import Path
from uuid import uuid4
import pandas as pd
from flask import request, flash, redirect, url_for, render_template, abort, current_app, jsonify
from flask_classful import FlaskView, route
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db, csrf
from app.forms.admin.project.Categories import ExcelCategoryForm, ImageCategoryForm
from app.forms.admin.project.ProjectAll import ProjectForm
from app.functions.store_excel import HandleExcel
from app.models.Database import Category
from app.models.Excel import ExcelRecord, ExcelColumn
from app.models.Project import Project


def get_category(category_id):
    return Category.query.filter_by(id=category_id).first_or_404()


class CategoryView(FlaskView):
    decorators = [login_required]

    @route('/store/<project_id>/<category_type>', methods=('POST', 'GET',))
    def create(self, project_id, category_type):
        form, url = None, None
        if category_type == 'excel':
            url = url_for('admin.CategoryView:create', project_id=project_id, category_type='excel')
            form = ExcelCategoryForm()
            if form.validate_on_submit():
                category = Category(title=form.title.data, description=form.description.data, type=category_type,
                                    project_id=project_id)
                f = form.excel.data
                filename = str(uuid4()) + '-' + secure_filename(f.filename)
                path = str(Path('excel_files', filename))
                file_path = Path(current_app.config['ASSETS_PATH'], path)
                f.save(file_path)
                category.file_path = str(file_path)
                category.save()
                excel = HandleExcel(file_path, category)
                excel.store_columns()
                excel.store_records()
                flash("Data was stored successfully", "success")
                return redirect(url_for("admin.AllProjectView:show", project_id=project_id))
            else:
                return render_template('admin/project_all/category/create.html', form=form, url=url)


        elif category_type == 'image':
            url = url_for('admin.CategoryView:create', category_type='image', project_id=project_id)
            form = ImageCategoryForm()

            if form.validate_on_submit():
                category = Category(description=form.description.data, title=form.title.data, project_id=project_id,
                                    type='image')
                category.create()
                flash('Category was created successfully', 'success')
                return redirect(url_for("admin.AllProjectView:show", project_id=project_id))
            else:
                return render_template('admin/project_all/category/create.html', form=form, url=url)
        else:
            abort(404)

    @route('category/<category_id>', methods=('GET',))
    def show(self, category_id):
        category = get_category(category_id)
        if category.type == 'excel':
            records = ExcelRecord.query.filter_by(category_id=category_id)
            df = pd.read_sql(records.statement, db.session.bind)
            df.drop(['CREATED_AT', 'UPDATED_AT', 'category_id', 'id'], axis=1, inplace=True)
            records = []
            for batch, df_batch in df.groupby('batch_id'):
                df_batch.drop(['batch_id', 'column_id'], axis=1, inplace=True)
                print(df_batch)
                records.append(df_batch.to_dict('list')['value'])
            return render_template('admin/project_all/category/show/excel.html', category=category, records=records)
        else:
            return render_template('admin/project_all/category/show/image.html', category=category)

    @route('/<category_id>/edit', methods=('GET',))
    def edit(self, category_id):
        project = get_category(category_id)
        form = ProjectForm(title=project.title, description=project.description)
        return render_template('admin/project_all/edit.html', form=form, category_id=category_id)

    @route('/update_column/<column_id>', methods=('POST',))
    @csrf.exempt
    def update_column(self, column_id):
        column = ExcelColumn.query.filter_by(id=column_id).first_or_404()
        column.title = request.form.get('title')
        column.description = request.form.get('description')
        column.save()
        flash('Column was updated successfully')
        return redirect(url_for('admin.CategoryView:show', category_id=column.category_id))

    @route('/<category_id>/update', methods=('POST',))
    def update(self, category_id):
        project = get_category(category_id)
        form = ProjectForm(request.form)
        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.save()
            flash("Project was updated successfully", "success")
            return redirect(url_for("admin.AllProjectView:index"))
        else:
            return redirect(request.url)

    @route('database/<project_id>/category/<category_id>/delete', methods=('POST',))
    def delete(self, project_id, category_id):
        category = get_category(category_id)
        category.delete()
        flash("Project was deleted successfully", 'success')
        return redirect(url_for('admin.AllProjectView:show', project_id=project_id))
