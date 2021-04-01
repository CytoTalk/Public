from pathlib import Path
from uuid import uuid4

from flask import request, flash, redirect, url_for, render_template, abort, current_app
from flask_classful import FlaskView, route
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.forms.admin.project_all.Categories import ExcelCategoryForm, ImageCategoryForm
from app.forms.admin.project_all.ProjectAll import ProjectAlLForm
from app.functions.store_excel import HandleExcel
from app.models.Category import Category
from app.models.Project import Project


def get_category(category_id):
    return Category.query.filter_by(id=category_id, type=1).first_or_404()


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


        elif category_type == 'image':
            url = url_for('admin.CategoryView:store', category_type='image')
            form = ImageCategoryForm()
        else:
            abort(404)
        return render_template('admin/project_all/category/create.html', form=form, url=url)

    @route('/store/<project_id>/<category_type>', methods=('POST',))
    def store(self, project_id, category_type):
        pass
        # if category_type == 'excel':
        #     form = ExcelCategoryForm(request.form)
        #     if not form.validate_on_submit():
        #         return redirect(
        #             url_for("admin.CategoryView:create", project_id=project_id, category_type=category_type))
        #
        #     category = Category(title=form.title.data, description=form.description.data, type=category_type)
        #     import pdb;
        #     pdb.set_trace()
        #
        #     filename = str(uuid4()) + '-' + secure_filename(form.excel.data)
        #     path = str(Path('excel_files', filename))
        #     file_path = Path(current_app.config['ASSETS_PATH'], path)
        #     form.file.data.save(file_path)
        #     category.save()
        #     excel = HandleExcel(file_path, category)
        #     excel.store_columns()
        #     flash("Data was stored successfully")
        #     return redirect(url_for("admin.AllProjectView:show", project_id=project_id))
        #
        # elif category_type == 'image':
        #     form = ImageCategoryForm()
        # else:
        #     abort(404)
        # return redirect(url_for("admin.CategoryView:index"))

    @route('category/<category_id>', methods=('GET',))
    def show(self, category_id):
        category = get_category(category_id)
        return render_template('admin/project_all/show.html', category=category)

    @route('/<category_id>/edit', methods=('GET',))
    def edit(self, category_id):
        project = get_category(category_id)
        form = ProjectAlLForm(title=project.title, description=project.description)
        return render_template('admin/project_all/edit.html', form=form, category_id=category_id)

    @route('/<category_id>/update', methods=('POST',))
    def update(self, category_id):
        project = get_category(category_id)
        form = ProjectAlLForm(request.form)
        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.save()
            flash("Project was updated successfully", "success")
            return redirect(url_for("admin.AllProjectView:index"))
        else:
            return redirect(request.url)

    @route('<category_id>/delete', methods=('POST',))
    def delete(self, category_id):
        project = get_category(category_id)
        project.delete()
        flash("Project was deleted successfully", 'success')
        return redirect(url_for('admin.AllProjectView:index'))
