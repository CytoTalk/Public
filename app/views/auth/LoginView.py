from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView,route
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.forms.auth.LoginForm import LoginForm
from app.models.User import User


class LoginView(FlaskView):

    def index(self):
        form = LoginForm()
        return render_template('auth/login.html', form=form)

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.LoginView:index'))
        login_user(user, remember=remember)
        return redirect(url_for('admin.dashboard'))

    @route('logout')
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('main.homepage'))
