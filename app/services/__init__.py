from flask import Blueprint

from app.views.services import ServiceView

service = Blueprint('services', __name__, )
ServiceView.register(service, trailing_slash=False)
