from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
from flask_cors import CORS
from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail
from flask_wtf import CSRFProtect

from app.main import main
from app.views.helpers import delete_files
from instance.config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

sched = BackgroundScheduler(daemon=True)
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
cors = CORS()


def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_object(config_options[config("APP_ENV")])
    db.init_app(app)
    login_manager.login_view = 'auth.LoginView:index'
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    sched.add_job(delete_files, 'interval', minutes=1, args=(app,))
    try:
        sched.start()
    except SchedulerAlreadyRunningError:
        pass
    from app.main import main as main_blueprint
    from app.auth import auth as auth_blueprint
    from app.admin import admin as admin_blueprint
    from app.database import database as database_blueprint
    from app.project import project as project_blueprint
    from app.feature import feature as feature_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(database_blueprint)
    app.register_blueprint(project_blueprint)
    app.register_blueprint(feature_blueprint)
    Bootstrap(app)
    return app
