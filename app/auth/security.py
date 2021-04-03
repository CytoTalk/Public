from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
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
