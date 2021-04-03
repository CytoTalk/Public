from flask import render_template
from flask_classful import FlaskView
from flask_login import login_required, current_user
from app.models.User import User


class UserView(FlaskView):
    decorators = [login_required]

    def index(self):
        users = User.query.filter(User.id != current_user.id)
        return render_template('admin/user/index.html', users=users)