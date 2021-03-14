from flask import Blueprint

project = Blueprint('project', __name__, url_prefix='/projects')
import app.views.project
