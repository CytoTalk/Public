from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app.main import main
from app.views.helpers import delete_files
from instance.config import config_options

sched = BackgroundScheduler(daemon=True)


def create_app(config_name='production'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_options[config_name])
    sched.add_job(delete_files, 'interval', minutes=1, args=(app,))
    sched.start()
    from app.main import main
    app.register_blueprint(main)
    return app
