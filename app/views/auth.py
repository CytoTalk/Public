from decouple import config
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.auth import auth
from flask import render_template, request, flash, redirect, url_for

from app.migrations.User import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@auth.route('/login', methods=('GET',))
def login_get():
    user = User.query.filter_by(email=config('ADMIN_EMAIL')).first()
    if user is None:
        admin = User(email=config('ADMIN_EMAIL'),
                     password=generate_password_hash(config('ADMIN_PASSWORD'), method='sha256'))

        db.session.add(admin)
        db.session.commit()
    return render_template('auth/login.html')


@auth.route('/login', methods=('POST',))
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'error')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('admin.dashboard'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
