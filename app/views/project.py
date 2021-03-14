from pathlib import Path

from flask import render_template, send_from_directory, current_app

from app.models.Image import Image
from app.models.Project import Project
from app.project import project


@project.route('/', methods=('GET',))
def index():
    projects = Project.query.all()
    print(projects)
    return render_template('project/index.html', projects=projects)


@project.route('/project/<project_id>', methods=('GET',))
def show(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    return render_template('project/show.html',project=project)


@project.route('/project/category/image/<image_id>', methods=('GET',))
def get_image(image_id):
    image = Image.query.filter_by(id=image_id).first_or_404()
    return send_from_directory(str(Path(current_app.config['ASSETS_PATH'])), filename=image.path, as_attachment=True)
