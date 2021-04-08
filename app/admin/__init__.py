from flask import Blueprint, render_template, abort

from app.views.admin.database.ProjectView import (ProjectUpdate, ProjectIndex, ProjectPost, ProjectCreate,
                                                  ProjectDelete,
                                                  ProjectEdit, ProjectShow)

from app.views.admin.database import DatabaseView
from app.views.admin.database.CategoryView import (CategoryUpdate, CategoryPost, CategoryCreate, CategoryDelete,
                                                   CategoryEdit, CategoryShow)
from app.views.admin.database.ImageView import (ImagePost, ImageCreate, ImageDelete, ImageShow)
from flask_login import login_required, current_user

from app.views.admin.UserView import UserView
from app.views.admin.project.CategoryView import CategoryView

admin = Blueprint('admin', __name__, url_prefix='/admin')
from app.views.admin.project.AllProjectView import AllProjectView


@admin.before_request
@login_required
def is_admin():
    if not current_user.is_admin:
        abort(401)


AllProjectView.register(admin, trailing_slash=False)
CategoryView.register(admin, trailing_slash=False)
UserView.register(admin, trailing_slash=False)
DatabaseView.register(admin, trailing_slash=False)

# Category Routes
admin.add_url_rule('/database/<project_id>/category/create', view_func=CategoryPost.as_view('category_store'),
                   methods=['POST'])
admin.add_url_rule('/database/<project_id>/category/create', view_func=CategoryCreate.as_view('category_create'),
                   methods=['GET'])
admin.add_url_rule('/database/category/<category_id>/', view_func=CategoryShow.as_view('category_show'),
                   methods=['GET'])
admin.add_url_rule('/database/category/<category_id>/edit', view_func=CategoryEdit.as_view('category_edit'),
                   methods=['GET'])
admin.add_url_rule('/database/category/<category_id>/edit', view_func=CategoryUpdate.as_view('category_update'),
                   methods=['POST'])
admin.add_url_rule('/database/category/<category_id>/delete', view_func=CategoryDelete.as_view('category_delete'),
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
