from flask import Blueprint

from app.views.project import ProjectView

project = Blueprint('project', __name__, url_prefix='/projects')
ProjectView.register(project, trailing_slash=False)

