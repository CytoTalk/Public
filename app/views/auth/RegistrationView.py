from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView
from werkzeug.security import generate_password_hash

from app.auth.security import hash_password
from app.email import send_verification_email
from app.forms.auth.RegistrationForm import RegistrationForm
from app.models.User import User


class RegistrationView(FlaskView):

    def index(self):
        form = RegistrationForm()
        return render_template('auth/register.html', form=form)

    def post(self):
        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("Email already exist, please use another email!",'error')
                return redirect(request.url)

            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hash_password(form.password.data))
            user.create()
            send_verification_email(user)
            flash("Account was created successfully", 'success')
            return redirect(url_for('auth.verify_email'))
        else:
            return render_template('auth/register.html', form=form)
