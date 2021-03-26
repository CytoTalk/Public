from decouple import config
from flask_login import login_user, login_required, logout_user
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.auth import auth
from flask import render_template, request, flash, redirect, url_for, abort

from app.forms.auth.ForgotPasswordForm import ForgotPasswordForm
from app.forms.auth.LoginForm import LoginForm
from app.forms.auth.RegistrationForm import RegistrationForm
from app.models.User import User


def generate_token(email:str):
    ts =  URLSafeTimedSerializer(config["SECRET_KEY"])
    return ts.dumps(email, salt='email-confirm-key')

def send_confirmation_email(to:str,token_url:str):
    html = render_template(
        'email/verify_email.html',
        confirm_url=token_url)
    send_email()

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@auth.route('/login', methods=('GET',))
def login_get():
    form = LoginForm()
    user = User.query.filter_by(email=config('ADMIN_EMAIL')).first()
    if user is None:
        admin = User(email=config('ADMIN_EMAIL'),
                     password=generate_password_hash(config('ADMIN_PASSWORD'), method='sha256'))

        db.session.add(admin)
        db.session.commit()
    return render_template('auth/login.html', form=form)


@auth.route('/login', methods=('POST',))
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'error')
        return redirect(url_for('auth.login_get'))
    login_user(user, remember=remember)
    return redirect(url_for('admin.dashboard'))


@auth.route('/register', methods=('GET',))
def register_get():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)


@auth.route('/register', methods=('POST',))
def register_post():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='sha256'))
        user.create()
        flash("Account was created successfully", 'success')
        token_url = url_for(
            'confirm_email',
            token=generate_token(user.email),
            _external=True)
        send_confirmation_email(user.email,token_url)
        return redirect(url_for('auth.verify_email'))
    else:
        return render_template('auth/register.html', form=form)


@auth.route('/forgot_password', methods=('GET',))
def forgot_password_get():
    form = ForgotPasswordForm()
    return render_template('auth/forgot_password.html', form=form)


@auth.route('/forgot_password', methods=('POST',))
def forgot_password_post():
    form = ForgotPasswordForm(request.form)
    if form.validate_on_submit():
        pass
    else:
        abort(403)


@auth.route('verify_email', methods=('GET',))
def verify_email():
    return render_template('auth/verify_email.html')

@auth.route('/verify_email/<token>',methods=('GET',))
def verify_token(token):
    pass



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
