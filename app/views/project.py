from pathlib import Path

import flask_login
from flask import send_from_directory, current_app, jsonify, abort
from flask import request, render_template
from flask_classful import FlaskView, route
from flask_cors import cross_origin
from flask_login import current_user
from sqlalchemy import text
from app import db, csrf
from app.auth.security import verify_project_permission
from app.models.Project import SubProject
from app.models.Excel import ExcelRecord
from app.models.Project import ImageStore as Image
from app.models.Project import Project


class ProjectView(FlaskView):
    """
    This is where editing begins
    """

    def index(self):

        projects = Project.query.filter_by(is_public=True).get()
        if current_user.is_authenticated:
            projects = Project.query.filter_by(is_public=False).get()
            for project in projects:
                if current_user in project.allowed_users:
                    projects.append(project)

        return render_template('front/project/index.html', projects=projects)

    @route('/<project_id>', methods=('GET',))
    @verify_project_permission
    def show(self, project_id):
        project = Project.query.filter_by(id=project_id).first_or_404()
        return render_template(
            'front/project/show/sub_project.html', project=project)

    @route('/subproject/<subproject_id>')
    def subproject(self, subproject_id):
        subproject = SubProject.query.filter_by(id=subproject_id).first_or_404()
        if subproject.type == 'excel':
            return render_template('front/project/show/excel.html', subproject=subproject)
        return render_template('front/project/show/image.html', subproject=subproject)

    @route('/get_column_data/<column_id>', methods=('GET',))
    @cross_origin()
    def get_column_data(self, column_id):
        value = request.args.get('value')
        query = ExcelRecord.query.filter_by(column_id=column_id)
        if value:
            result = query.filter(ExcelRecord.value.like(f"%{value}%")).limit(10).all()
        else:
            result = query.limit(10).all()
        return jsonify(results=[e.serialize() for e in result])

    @route('/handle_excel_records/<subproject_id>', methods=('POST', 'GET',))
    @cross_origin()
    @csrf.exempt
    def handle_excel_records(self, subproject_id):
        if request.method == 'GET':
            sql = text(
                f"select batch_id,array_agg(value order by column_id) as values from excel_records where subproject_id={subproject_id} group by batch_id limit(10) ")
            result = db.engine.execute(sql)
            return jsonify(result=[list(x) for x in result])
        else:
            conditions = []
            for key, value in request.form.items():
                conditions.append(f"(values::text like '%{value}%')")
            params = " and ".join(conditions)
            sql = text(
                f"select * from (select batch_id,array_agg(value order by column_id) as values from excel_records  group by batch_id) as s where {params}")
            result = db.engine.execute(sql)
            return jsonify(result=[list(x) for x in result])

    @route('/subproject/image/<image_id>', methods=('GET',))
    def get_image(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        return send_from_directory(str(Path(current_app.config['ASSETS_PATH'])), filename=image.path,
                                   as_attachment=True)

    @route('/project/<project_id>/images', methods=('GET',))
    def show_project_images(self, project_id):
        project = Project.query.filter_by(id=project_id).first_or_404()
        categories = SubProject.query.filter_by(project_id=project_id, type='image').all()
        return render_template('front/project/show.html', project=project, categories=categories)
