from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.background import BackgroundScheduler
from flask_login import LoginManager
from flask import Flask
from app.main import main
from app.views.helpers import delete_files
from instance.config import config_options
from flask_sqlalchemy import SQLAlchemy

sched = BackgroundScheduler(daemon=True)
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='production'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_options[config_name])
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    sched.add_job(delete_files, 'interval', minutes=1, args=(app,))
    try:
        sched.start()
    except SchedulerAlreadyRunningError:
        pass
    from app.main import main as main_blueprint
    from app.auth import auth as auth_blueprint
    from app.admin import admin as admin_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    return app
