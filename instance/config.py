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
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{config("DB_USER")}:{config("DB_PASSWORD")}@localhost/{config("DB_NAME")}'
    if os.environ.get('GITHUB_WORKFLOW'):
        SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:postgres@127.0.0.1/github_actions'

    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    UPLOAD_FOLDER = Path.joinpath(PROJECT_PATH, 'uploads')


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class ProdConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
