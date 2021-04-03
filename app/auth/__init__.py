from flask import Blueprint

from app.views.auth import LoginView, RegistrationView, ResetPasswordView, VerificationView

auth = Blueprint('auth', __name__)


LoginView.LoginView.register(auth, trailing_slash=False)
RegistrationView.RegistrationView.register(auth, trailing_slash=False, route_base='/register')
ResetPasswordView.ResetPasswordView.register(auth, trailing_slash=False)
VerificationView.VerificationView.register(auth, trailing_slash=False)
