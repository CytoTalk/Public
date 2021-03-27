from decouple import config
from flask import render_template, url_for
from flask_mail import Message
from app import mail
from app.models.User import User
from app.token import generate_confirmation_token


def send_email(to: str, subject: str, template: str):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=config('MAIL_DEFAULT_SENDER')
    )
    return mail.send(msg)


def send_verification_email(user: User):
    token = generate_confirmation_token(user.email)
    url = url_for('auth.VerificationEmail:get', token=token, _external=True)
    html = render_template(
        'email/verify_email.html',
        confirm_url=url)
    return send_email(to=user.email, template=html, subject="Verify your email")


def send_password_reset_email(user: User):
    token = generate_confirmation_token(user.email)
    url = url_for('auth.ResetPasswordView:get', token=token, _external=True)
    html = render_template(
        'email/reset_password.html',
        password_reset_url=url)
    return send_email(to=user.email, template=html, subject="Verify your email")
