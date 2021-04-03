from pathlib import Path

from flask import render_template, send_from_directory, current_app, jsonify
from flask_classful import FlaskView
from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView, route
from flask_cors import cross_origin
from flask_login import login_required

from app.functions.store_excel import HandleExcel
from app.models.Category import Category
from app.models.Excel import ExcelRecord
from app.models.Image import Image
from app.models.Project import Project


class ProjectView(FlaskView):
    def index(self):
        projects = Project.query.all()
        print(projects)
        return render_template('project/index.html', projects=projects)

    @route('/<project_id>', methods=('GET',))
    def show(self, project_id):
        project = Project.query.filter_by(id=project_id).first_or_404()
        if project.type == 'combined':
            return render_template('project/show/category.html', project=project)
        return render_template('project/show.html', project=project)

    @route('/category/<category_id>')
    def category(self, category_id):
        category = Category.query.filter_by(id=category_id).first_or_404()
        if category.type == 'excel':
            return render_template('project/show/excel.html', category=category)

    @route('/get_column_data/<column_id>', methods=('GET',))
    @cross_origin()
    def get_column_data(self, column_id):
        value = request.args.get('value')
        query = ExcelRecord.query.filter_by(column_id=column_id)
        if value:
            print("value is here")
            result = query.filter(ExcelRecord.value.like(f"%{value}%")).limit(10).all()
        else:
            result = query.limit(10).all()

        return jsonify(results=[e.serialize() for e in result])

    @route('/handle_excel_records', methods=['POST'])
    def handle_excel_records(self):
        pass


    @route('/category/image/<image_id>', methods=('GET',))
    def get_image(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        return send_from_directory(str(Path(current_app.config['ASSETS_PATH'])), filename=image.path,
                                   as_attachment=True)
