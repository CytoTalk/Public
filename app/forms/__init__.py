from datetime import timedelta

from decouple import config
from wtforms import Form
from wtforms.csrf.session import SessionCSRF


class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = config("SECRET_KEY")
        csrf_time_limit = timedelta(minutes=20)
