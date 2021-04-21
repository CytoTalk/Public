from flask import Blueprint, render_template
from flask_login import current_user

from app.views.auth import LoginView, RegistrationView, ResetPasswordView, VerificationView
from functools import wraps

auth = Blueprint('auth', __name__)


def user_is_active(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and not current_user.is_active:
            return render_template('auth/account_closed.html')
        return function(*args, **kwargs)
    return wrapper


LoginView.LoginView.register(auth, trailing_slash=False)
# RegistrationView.RegistrationView.register(auth, trailing_slash=False, route_base='/register')
# ResetPasswordView.ResetPasswordView.register(auth, trailing_slash=False)
# VerificationView.VerificationView.register(auth, trailing_slash=False)
