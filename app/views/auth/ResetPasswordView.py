from flask import request, flash, redirect, url_for, render_template, abort
from flask_classful import FlaskView, route
from flask_login import login_required, login_user, current_user

from app.email import send_password_reset_email
from app.forms.auth.ForgotPasswordForm import ForgotPasswordForm
from app.forms.auth.ResetPasswordForm import ResetPasswordForm
from app.models.User import User
from app.token import confirm_token
from app.auth.security import hash_password


class ResetPasswordView(FlaskView):

    def index(self):
        form = ForgotPasswordForm()
        return render_template('auth/forgot_password.html', form=form)

    def post(self):
        form = ForgotPasswordForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
                flash("A password reset link has been sent to your email", "success")
                return redirect(url_for("main.homepage"))
            else:
                flash("A user with the specified email address does not exist!", 'error')
                redirect(url_for("ResetPasswordView:index"))
        else:
            abort(403)

    def get(self, token):
        try:
            email = confirm_token(token)
        except:
            flash('The reset link is invalid or has expired.', 'error')
            return redirect(url_for('main.homepage'))

        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for("auth.ResetPasswordView:reset_password"))

    @route('/reset_password', methods=('GET',))
    @login_required
    def reset_password(self):
        form = ResetPasswordForm()
        return render_template('auth/reset_password.html', form=form)

    @route('/update_password', methods=('POST',))
    @login_required
    def update_password(self):
        form = ResetPasswordForm(request.form)
        if form.validate_on_submit():
            current_user.password = hash_password(form.password.data)
            current_user.save()
            flash("Password was updated successfully!", "success")
            return redirect(url_for("main.homepage"))
        else:
            for error in form.errors:
                for message in error:
                    flash(message, "error")
                return redirect(request.url)
