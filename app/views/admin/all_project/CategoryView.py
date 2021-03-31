from flask import request, flash, redirect, url_for, render_template, abort
from flask_classful import FlaskView, route
from flask_login import login_required

from app.forms.admin.project_all.Categories import ExcelCategoryForm, ImageCategoryForm
from app.forms.admin.project_all.ProjectAll import ProjectAlLForm
from app.functions.store_excel import HandleExcel
from app.models.Category import Category
from app.models.Project import Project


def get_category(category_id):
    return Category.query.filter_by(id=category_id, type=1).first_or_404()


class CategoryView(FlaskView):
    decorators = [login_required]

    def create(self, project_id, category_type):
        form, url = None, None
        if category_type == 'excel':
            url = url_for('admin.CategoryView:store', project_id=project_id, category_type='excel')
            form = ExcelCategoryForm()
        elif category_type == 'image':
            url = url_for('admin.CategoryView:store', category_type='image')
            form = ImageCategoryForm()
        else:
            abort(404)
        return render_template('admin/project_all/category/create.html', form=form, url=url)

    @route('/<project_id>/<category_type>', methods=('POST',))
    def store(self, project_id, category_type):
        if category_type == 'excel':
            form = ExcelCategoryForm(request.form)
            excel = HandleExcel()
        elif category_type == 'image':
            form = ImageCategoryForm()
        else:
            abort(404)
        return redirect(url_for("admin.CategoryView:index"))

    @route('/<category_id>', methods=('GET',))
    def show(self, category_id):
        project = get_category(category_id)
        return render_template('admin/project_all/show.html', project=project)

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
