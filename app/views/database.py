from pathlib import Path

from flask import send_from_directory, current_app
from flask import render_template
from flask_classful import FlaskView, route
from app.models.Database import DatabaseCategory as Category
from app.models.Database import Image
from app.models.Project import Project


class DatabaseView(FlaskView):
    def index(self):
        databases = Project.query.all()
        print(databases)
        return render_template('app/templates/front/database/index.html', databases=databases)

    @route('/<database_id>', methods=('GET',))
    def show(self, database_id):
        database = Project.query.filter_by(id=database_id).first_or_404()
        categories = Category.query.filter_by(database_id=database_id).all()
        return render_template('app/templates/front/database/show.html', database=database, categories=categories)

    @route('/subproject/image/<image_id>', methods=('GET',))
    def get_image(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        return send_from_directory(str(Path(current_app.config['ASSETS_PATH'])), filename=image.path,
                                   as_attachment=True)

    @route('/database/<database_id>/images', methods=('GET',))
    def show(self, database_id):
        database = Project.query.filter_by(id=database_id).first_or_404()
        return render_template('app/templates/front/database/show.html', database=database)
