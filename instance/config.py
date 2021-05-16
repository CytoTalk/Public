# import os
import os
from pathlib import Path
from decouple import config


# base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'YKfmc2TpC1NP63m4wnBg6nyHYKfOGI4nss'
    PROJECT_PATH = Path(__file__).parent.parent
    OUTPUT_PATH = Path.joinpath(PROJECT_PATH, 'output_location')
    ASSETS_PATH = Path.joinpath(PROJECT_PATH, 'assets')
    IMAGES_PATH = Path.joinpath(ASSETS_PATH, 'images')
    STATIC_PATH = Path.joinpath(PROJECT_PATH, 'app', 'static')
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    ALLOWED_IMAGE_FILES = {'jpg', 'png', 'jpeg', 'gif'}
    UPLOAD_FOLDER = Path.joinpath(PROJECT_PATH, 'uploads')

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{config("DB_USER")}:{config("DB_PASSWORD")}@localhost/{config("DB_NAME")}'
    if os.environ.get('GITHUB_WORKFLOW'):
        SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:postgres@127.0.0.1/github_actions'

    ###########################################
    # Mail config

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEBUG = config('APP_DEBUG')
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = config('MAIL_DEFAULT_SENDER')

    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT')


class DevConfig(Config):
    DEBUG = config('APP_DEBUG')
    MAIL_DEBUG = config('APP_DEBUG')
    DEVELOPMENT = True


class ProdConfig(Config):
    DEVELOPMENT = False
    MAIL_USE_SSL = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
