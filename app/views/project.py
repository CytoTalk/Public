from pathlib import Path

from flask import render_template, send_from_directory, current_app, jsonify
from flask_classful import FlaskView
from flask import request, flash, redirect, url_for, render_template
from flask_classful import FlaskView, route
from flask_cors import cross_origin
from flask_login import login_required
from sqlalchemy import text

from app import db, csrf
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
            image_category = Category.query.filter_by(project_id=project_id, type='image').first() is not None
            excel_categories = Category.query.filter_by(project_id=project_id, type='excel').all()
            return render_template(
                'project/show/category.html', project=project, image_category=image_category,
                excel_categories=excel_categories)
        else:
            categories = Category.query.filter_by(project_id=project_id).all()
            return render_template('project/show.html', project=project, categories=categories)

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
            result = query.filter(ExcelRecord.value.like(f"%{value}%")).limit(10).all()
        else:
            result = query.limit(10).all()

        return jsonify(results=[e.serialize() for e in result])

    @route('/handle_excel_records/<category_id>', methods=('POST', 'GET',))
    @cross_origin()
    @csrf.exempt
    def handle_excel_records(self, category_id):
        if request.method == 'GET':
            sql = text(
                f"select batch_id,array_agg(value order by column_id) as values from excel_records where category_id={category_id} group by batch_id limit(10) ")
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

        return jsonify(HandleExcel.handle_query(dict(category_id=13)))

    @route('/category/image/<image_id>', methods=('GET',))
    def get_image(self, image_id):
        image = Image.query.filter_by(id=image_id).first_or_404()
        return send_from_directory(str(Path(current_app.config['ASSETS_PATH'])), filename=image.path,
                                   as_attachment=True)

    @route('/project/<project_id>/images', methods=('GET',))
    def show_project_images(self, project_id):
        project = Project.query.filter_by(id=project_id).first_or_404()
        categories = Category.query.filter_by(project_id=project_id, type='image').all()
        return render_template('project/show.html', project=project, categories=categories)
