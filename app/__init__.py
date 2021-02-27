from flask import Flask

from app.main import main
from instance.config import config_options


def create_app(config_name='production'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_options[config_name])
    from app.main import main
    app.register_blueprint(main)
    return app
