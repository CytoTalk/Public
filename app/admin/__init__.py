from flask import Blueprint, render_template, abort

from app.views.admin.ProjectView import (ProjectUpdate, ProjectIndex, ProjectPost, ProjectCreate, ProjectDelete,
                                         ProjectEdit, ProjectShow)
from app.views.admin.CategoryView import (CategoryUpdate, CategoryPost, CategoryCreate, CategoryDelete,
                                          CategoryEdit, CategoryShow)
from app.views.admin.ImageView import (ImagePost, ImageCreate, ImageDelete, ImageShow)
from flask_login import login_required, current_user

from app.views.admin.UserView import UserView
from app.views.admin.all_project.CategoryView import CategoryView

admin = Blueprint('admin', __name__, url_prefix='/admin')
from app.views.admin.all_project.AllProjectView import AllProjectView


@admin.before_request
@login_required
def is_admin():
    if not current_user.is_admin:
        abort(401)


AllProjectView.register(admin, trailing_slash=False)
CategoryView.register(admin, trailing_slash=False)
UserView.register(admin, trailing_slash=False)

# Project Routes
admin.add_url_rule('/projects/', view_func=ProjectIndex.as_view('project_index'), methods=['GET'])
admin.add_url_rule('/projects/create', view_func=ProjectPost.as_view('project_store'), methods=['POST'])
admin.add_url_rule('/projects/create', view_func=ProjectCreate.as_view('project_create'), methods=['GET'])
admin.add_url_rule('/projects/<project_id>/', view_func=ProjectShow.as_view('project_show'), methods=['GET'])
admin.add_url_rule('/projects/<project_id>/edit', view_func=ProjectEdit.as_view('project_edit'), methods=['GET'])
admin.add_url_rule('/projects/<project_id>/edit', view_func=ProjectUpdate.as_view('project_update'), methods=['POST'])
admin.add_url_rule('/projects/<project_id>/delete', view_func=ProjectDelete.as_view('project_delete'), methods=['POST'])

# Category Routes
admin.add_url_rule('/project/<project_id>/category/create', view_func=CategoryPost.as_view('category_store'),
                   methods=['POST'])
admin.add_url_rule('/project/<project_id>/category/create', view_func=CategoryCreate.as_view('category_create'),
                   methods=['GET'])
admin.add_url_rule('/project/category/<category_id>/', view_func=CategoryShow.as_view('category_show'), methods=['GET'])
admin.add_url_rule('/project/category/<category_id>/edit', view_func=CategoryEdit.as_view('category_edit'),
                   methods=['GET'])
admin.add_url_rule('/project/category/<category_id>/edit', view_func=CategoryUpdate.as_view('category_update'),
                   methods=['POST'])
admin.add_url_rule('/project/category/<category_id>/delete', view_func=CategoryDelete.as_view('category_delete'),
                   methods=['POST'])

# Image Routes
admin.add_url_rule('/<category_id>/category/create', view_func=ImagePost.as_view('image_store'), methods=['POST'])
admin.add_url_rule('/<category_id>/category/create', view_func=ImageCreate.as_view('image_create'), methods=['GET'])
admin.add_url_rule('/category/<image_id>/', view_func=ImageShow.as_view('image_show'), methods=['GET'])
admin.add_url_rule('/category/<image_id>/delete', view_func=ImageDelete.as_view('image_delete'), methods=['POST'])


@admin.route('/dashboard', methods=('GET',))
@login_required
def dashboard():
    return render_template('admin/dashboard.html')
