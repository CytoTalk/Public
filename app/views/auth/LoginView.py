from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView, route
from flask_login import login_user, logout_user, login_required, current_user
# from werkzeug.security import check_password_hash
from app.forms.auth.LoginForm import LoginForm
from app.models.User import User


class LoginView(FlaskView):

    @route('/', methods=('GET', 'POST'))
    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for('main.homepage'))
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember_me.data
            user = User.query.filter_by(email=email, password=password).first()

            # if not user or not check_password_hash(user.password, password):
            if not user:
                flash('Please check your login details and try again.', 'error')
                return redirect(request.url)
            if not user.is_active:
                return render_template('auth/account_closed.html')
            login_user(user, remember=remember)

            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.homepage'))
        return render_template('auth/login.html', form=form)

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('main.homepage'))
