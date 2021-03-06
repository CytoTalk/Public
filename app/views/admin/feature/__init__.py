from io import BytesIO

from flask import request, flash, redirect, url_for, render_template, current_app, make_response
from flask_classful import FlaskView, route
from sqlalchemy import text
from werkzeug.utils import secure_filename

from app.forms.admin.feature import FeatureForm, ColumnForm
from app.models.Feature import Feature as FeatureModel, DATA_TYPES_MAPPER
from app.views.helpers import save_file
from pathlib import Path
import pandas as pd


def get_feature(feature_id) -> FeatureModel:
    return FeatureModel.query.filter_by(id=feature_id).first_or_404()


def insert_feature_data(feature: FeatureModel):
    form = request.form.to_dict()
    data = handle_record_form_data(feature, form)
    if len(data):
        sql = "INSERT INTO %s (%s) VALUES(%s)" % (
            f"feature_table_{feature.id}", ",".join(data.keys()), ",".join(f"'{x}'" for x in data.values()))
        try:
            feature.execute_query(sql)
            flash("Record was created successfully", "success")
        except Exception as e:
            flash(str(e), "error")
    else:
        flash("Please fill at least one column", 'error')


def edit_feature_data(feature: FeatureModel, record_id: int):
    form = request.form.to_dict()
    data = handle_record_form_data(feature, form)
    if len(data):
        key_pair_values = [f"{key}='{value}'" for key, value in data.items()]
        sql = f"UPDATE feature_table_{feature.id} SET \n" \
              f"{','.join(key_pair_values)}\n" \
              f"WHERE i_d={record_id}" \
              f";"
        try:
            print(sql)
            feature.execute_query(text(sql))
            flash("Record was updated successfully", "success")
        except Exception as e:
            flash(str(e), "error")
    else:
        flash("Please fill at least one column", 'error')


def handle_record_form_data(feature, form):
    data = {}
    for column in feature.columns['columns']:
        if column['data_type']['HTML'] == 'file':
            file = request.files[column['column_name']]
            if file:
                file_name = save_file(file, Path.joinpath(current_app.config['STATIC_PATH'], 'feature_images'),
                                      True)
            else:
                file_name = "none"
            data[column['column_name']] = url_for('static', filename="feature_images/" + file_name, _external=True)
            continue
        if column['data_type']['HTML'] == 'checkbox':
            data[column['column_name']] = column['column_name'] in form
            continue
        if form[column['column_name']]:
            data[column['column_name']] = form[column['column_name']]
    return data


class FeatureView(FlaskView):
    route_prefix = '/projects/'

    @route('/', methods=('GET',))
    def index(self):
        features = FeatureModel.query.all()
        return render_template('admin/feature/index.html', features=features)

    @route('/create', methods=('POST', 'GET',))
    def create(self):
        form = FeatureForm()
        if form.validate_on_submit():
            feature = FeatureModel(
                title=form.title.data,
                description=form.description.data,
                is_public=form.status.data)
            feature.create()
            feature.make_db()
            flash("Feature Project was created successfully", "success")
            return redirect(url_for("admin.FeatureView:index"))
        return render_template('admin/feature/create.html', form=form)

    @route('/<feature_id>/create_column', methods=('GET', 'POST',))
    def create_column(self, feature_id):
        feature = get_feature(feature_id)
        form = ColumnForm()
        if form.validate_on_submit():
            try:
                feature.add_column(form.name.data, form.data_type.data, form.description.data)
                flash("Column was created successfully", "success")
                return redirect(url_for('admin.SubProjectView:show', subproject_id=feature.subproject_id))
            except Exception as e:
                flash(str(e), "error")
        return render_template('admin/feature/create.html', form=form)

    @route('/<feature_id>/edit_column/<column_name>', methods=('GET', 'POST',))
    def update_column(self, feature_id, column_name):
        feature = get_feature(feature_id)
        column = feature.get_column_data(column_name)
        data_type = [x for x in DATA_TYPES_MAPPER.keys() if DATA_TYPES_MAPPER[x] == column['data_type']][0]

        form = ColumnForm(name=column['original_name'], description=column['description'],
                          data_type=data_type, disabled=True)
        if form.validate_on_submit():
            feature.update_column(column_name=column_name, new_name=form.name.data, description=form.description.data)
            flash("Column was updated successfully", "success")
            return redirect(url_for('admin.SubProjectView:show', subproject_id=feature.subproject_id))
        return render_template('admin/feature/create.html', form=form)

    @route('/<feature_id>/show', methods=('GET',))
    def show(self, feature_id):
        feature = get_feature(feature_id)
        return render_template('admin/feature/show.html', feature=feature)

    @route('/<feature_id>/update', methods=("GET", "POST",))
    def update(self, feature_id):
        feature = get_feature(feature_id)

        form = FeatureForm(title=feature.title, description=feature.description, is_public=feature.is_public)
        if form.validate_on_submit():
            feature.title = form.title.data
            feature.description = form.description.data
            feature.is_public = not form.status.data
            feature.save()
            flash("Feature was updated successfully", "success")
            return redirect(url_for("admin.FeatureView:index"))
        return render_template('admin/feature/edit.html', form=form, feature_id=feature_id)

    @route('/<feature_id>/delete_column/<column_name>', methods=('POST',))
    def delete_column(self, feature_id, column_name):
        feature = get_feature(feature_id)
        feature.delete_column(column_name)
        flash("Column was deleted successfully", 'success')
        return redirect(url_for('admin.SubProjectView:show', subproject_id=feature.subproject_id))

    @route('/<feature_id>/delete', methods=('POST',))
    def delete(self, feature_id):
        feature = get_feature(feature_id)
        feature.delete()
        flash("Feature was deleted successfully", 'success')
        return redirect(url_for('admin.FeatureView:index'))

    @route('/<feature_id>/add_data', methods=('POST',))
    def add_data(self, feature_id):
        feature = get_feature(feature_id)
        insert_feature_data(feature)

        return redirect(url_for('admin.SubProjectView:show', subproject_id=feature.subproject_id))

    @route('/<feature_id>/upload_image', methods=['GET', 'POST'])
    def upload(self, feature_id):
        feature = get_feature(feature_id)
        if request.method == 'POST':
            key_column = request.form['key_column']
            files = request.files.get('files')
            for file in files:
                file_name = Path(file).stem
                new_file_name = save_file(file, current_app.config['IMAGES_PATH'], True)
                sql = f"UPDATE feature_table_{feature.id} set '{key_column}'=\
                 '{new_file_name}' WHERE {key_column}='{file_name}'"
                feature.execute_query(sql)

    @route('/<feature_id>/download', methods=('GET',))
    def download(self, feature_id):
        feature = get_feature(feature_id)
        columns = [column['column_name'] for column in feature.columns['columns']]
        data = feature.fetch_records().fetchall()
        df = pd.DataFrame(list(data))
        df.drop(df.columns[[0]], axis=1, inplace=True)  # df.columns is zero-based pd.Index
        df.columns = columns

        buffer = BytesIO()
        buffer.seek(0)
        df.to_excel(buffer, sheet_name='data', index=False)
        resp = make_response(buffer.getvalue())
        resp.headers['Content-Disposition'] = f'attachment; filename={secure_filename(feature.subproject.title)}.xlsx'
        resp.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return resp

    @route('<feature_id>/batch_upload', methods=('POST',))
    def batch_upload(self, feature_id):
        feature = get_feature(feature_id)
        file = request.files['file']
        key_column = request.form.get('key_column')
        df = pd.read_excel(file, index_col=False)
        df.columns = df.columns.str.lower()
        try:
            for index, row in df.iterrows():
                update_values = ",".join(f"'{x}'" for k, x in row.items())
                sql = f"CREATE OR REPLACE FUNCTION upsert() RETURNS void AS $$ \n" \
                      f"begin \n" \
                      f"IF EXISTS(SELECT * FROM feature_table_{feature_id} WHERE {key_column} = '{row[key_column]}') THEN \n \
                        update feature_table_{feature_id} set ({','.join(row.keys())}) = ({update_values}) where {key_column} = '{row[key_column]}';\n \
                        ELSE \n \
                        INSERT INTO feature_table_{feature_id}({','.join(row.keys())}) values({update_values});\n \
                        END IF; \n" \
                      f"end \n" \
                      f"$$ LANGUAGE plpgsql;\n" \
                      f"select upsert()"
                feature.execute_query(text(sql))
            flash("Data was uploaded successfully!", "success")

        except Exception as e:
            flash(str(e), 'error')
        return redirect(url_for('admin.SubProjectView:show', subproject_id=feature.subproject_id))

    @route('/<feature_id>/upload_images', methods=('POST',))
    def batch_upload_image(self, feature_id):
        feature = get_feature(feature_id)
        key_column = request.form.get('key_column')
        target_column = request.form.get('target_column')
        images = request.files.getlist('images')
        try:
            for image in images:
                file_name = str(Path(image.filename).stem)
                image_path = save_file(image, Path.joinpath(current_app.config['STATIC_PATH'], 'feature_images'),
                                       True)
                image_url = url_for('static', filename="feature_images/" + image_path, _external=True)
                sql = f"CREATE OR REPLACE FUNCTION upsert() RETURNS void AS $$ \n" \
                      f"begin \n" \
                      f"IF EXISTS(SELECT * FROM feature_table_{feature_id} WHERE {key_column} = '{file_name}') THEN \n \
                        update feature_table_{feature_id} set {target_column} = '{image_url}' where {key_column} = '{file_name}';\n \
                        ELSE \n \
                        INSERT INTO feature_table_{feature_id}({key_column},{target_column}) values('{file_name}','{image_url}');\n \
                        END IF; \n" \
                      f"end \n" \
                      f"$$ LANGUAGE plpgsql;\n" \
                      f"select upsert()"
                feature.execute_query(text(sql))
            flash("Images were uploaded successfully")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for('admin.SubProjectView:show', subproject_id=feature.subproject_id))
