import datetime

from flask import flash, redirect, url_for, render_template
from flask_classful import FlaskView
from flask_login import current_user, login_required
from app import auth
from app.email import send_verification_email
from app.models.Project import User
from app.token import confirm_token


class VerificationView(FlaskView):
    @login_required
    def index(self):
        send_verification_email(current_user)
        flash("A verification email has been sent to your account")
        return render_template('auth/verify_email.html')

    def get(self, token):
        try:
            email = confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'error')
            return redirect(url_for('main.homepage'))

        user = User.query.filter_by(email=email).first_or_404()
        if user.email_verified_at:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.confirmed = True
            user.email_verified_at = datetime.datetime.now()
            user.save()
            flash('Your email has been confirmed successfully. Thanks!', 'success')
        return redirect(url_for('auth.LoginView:index'))

