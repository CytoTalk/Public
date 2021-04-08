from flask import Blueprint, render_template, abort


from app.views.admin.database import DatabaseView

from flask_login import login_required, current_user
from app.views.admin.UserView import UserView
from app.views.admin.project.SubProjectView import SubProjectView
from app.views.admin.project import ProjectView
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
@login_required
def is_admin():
    if not current_user.is_admin:
        abort(401)


ProjectView.register(admin, trailing_slash=False)
SubProjectView.register(admin, trailing_slash=False)
UserView.register(admin, trailing_slash=False)
DatabaseView.register(admin, trailing_slash=False)

@admin.route('/', methods=('GET',))
@login_required
def dashboard():
    return render_template('admin/dashboard.html')
