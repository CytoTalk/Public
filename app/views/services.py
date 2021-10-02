from flask import render_template
from flask_classful import FlaskView, route

from app.models.Service import Service


class ServiceView(FlaskView):
    """
    This is where editing begins
    """

    @route('/', methods=('GET',))
    def index(self):
        services = Service.query.all()

        return render_template('front/service/index.html', services=services)

    @route('/<service_slug>', methods=('GET',))
    def show(self, service_slug):
        service = Service.query.filter_by(slug=service_slug).first_or_404()
        return render_template(
            'front/service/show.html', service=service)
