from flask import Blueprint
from app.views.database import DatabaseView

database = Blueprint('database', __name__, url_prefix='/databases')
DatabaseView.register(database, trailing_slash=False)

