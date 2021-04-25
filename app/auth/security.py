from functools import wraps

from flask import flash, redirect, url_for, abort
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.models.Project import Project
from app.models.User import User


def hash_password(password: str):
    return generate_password_hash(password, method='sha256')


def confirm_password(hashed_password: str, naked_password: str):
    return check_password_hash(hashed_password, naked_password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def email_verified(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


def verify_project_permission(func):
    @wraps(func)
    def decorated_function(project_id, *args, **kwargs):
        project = Project.query.get(project_id)
        if project and current_user.is_athenticated and not project.is_public and current_user in project.allowed_users:
            return func(project_id, *args, **kwargs)
        return abort(403, "You are not allowed to view this item")

    return decorated_function
