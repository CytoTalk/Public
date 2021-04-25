from functools import wraps

from flask import flash, redirect, url_for, abort
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.models.Project import Project, SubProject
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
    def decorated_function(*args, **kwargs):
        project = Project.query.get(kwargs['project_id'])
        if project.is_public or (project and current_user.is_authenticated and not project.is_public and project.id in [permitted.project_id
                                                                                                  for permitted in
                                                                                                  current_user.project_permissions]):
            return func(*args, **kwargs)
        return abort(403, "You are not allowed to view this item")

    return decorated_function


def verify_sub_project_permission(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        sub_project = SubProject.query.get(kwargs['subproject_id'])
        project = sub_project.project
        if project.is_public or (project and current_user.is_authenticated and not project.is_public and project.id in [permitted.project_id
                                                                                                  for permitted in
                                                                                                  current_user.project_permissions]):
            return func(*args, **kwargs)
        return abort(403, "You are not allowed to view this item")

    return decorated_function
