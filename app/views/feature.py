from io import BytesIO

import pandas as pd
from flask import jsonify, make_response, url_for, abort
from flask import request, render_template
from flask_classful import FlaskView, route
from flask_cors import cross_origin
from flask_paginate import get_page_args
from sqlalchemy import text
from werkzeug.utils import secure_filename, redirect

from app import csrf, db
from app.models.Feature import Feature
from app.views.admin.feature import get_feature, insert_feature_data, edit_feature_data


def fetch_record_post(feature: Feature, per_page: int, offset: int):
    conditions = []
    form = request.args.to_dict()
    for column in feature.columns['columns']:
        # """Handle numeric columns(Floats and Ints)"""
        if column['column_name'] not in form: continue
        statement = ""
        if column['data_type']['HTML'] == 'number':
            try:
                low = form[column['column_name'] + '_min'] if column['column_name'] + '_min' in form else None
                high = form[column['column_name'] + '_max'] if column['column_name'] + '_max' in form else None
                values = [low, high]
            except IndexError:
                continue
            if not low and not high:
                continue
            cast = 'integer' if column['data_type']['PYTHON'] == 'int' else 'float'

            if low and not high:
                statement = f"({column['column_name']}::{cast} >= {min(values)})"
            elif high and not low:
                statement = f"({column['column_name']}::{cast} <= {max(values)})"
            else:
                statement = f"({column['column_name']}::{cast} between {min(values)} and {max(values)})"
        # """Handle checkbox columns"""
        elif column['data_type']['HTML'] == 'checkbox':
            if form[column['column_name']] != 'all':
                statement = f"{column['column_name']} ={form[column['column_name']]}"
        elif column['data_type']['HTML'] == 'text' and form[column['column_name']]:
            if form[column['column_name']] != 'all':
                if form[column['column_name']] == 'null':
                    statement = f"({column['column_name']} is null)"
                else:
                    statement = f"({column['column_name']}::text = '{form[column['column_name']]}')"
        else:
            continue
        if statement:
            conditions.append(statement)
    params = " and ".join(conditions)
    limit_and_offset = f" limit {per_page} offset {offset}"
    if "_download" in request.args and int(form['_download']):
        limit_and_offset = f""
    if params:
        sql = text(
            f"select *, count(*) OVER() AS total_count from feature_table_{feature.id} where {params} ORDER BY i_d {limit_and_offset}")
    else:
        sql = text(f"select * , count(*) OVER() AS total_count from feature_table_{feature.id} ORDER BY i_d {limit_and_offset}")
    return sql


class FeatureView(FlaskView):
    """
    This is where editing begins
    """

    def index(self):
        # features = Feature.query.filter_by(is_public=True)
        features = Feature.query.all()

        return render_template('front/feature/index.html', features=features)

    @route('/<feature_id>', methods=('GET',))
    def show(self, feature_id):
        feature = Feature.query.filter_by(id=feature_id).first_or_404()
        return render_template(
            'front/feature/show.html', feature=feature)

    @route('<feature_id>/get_column_data/<column_name>', methods=('GET',))
    @cross_origin()
    def get_column_data(self, feature_id, column_name):
        feature = get_feature(feature_id)
        column = feature.get_column_data(column_name)
        value = request.args.get('value')
        if value:

            sql = f"SELECT DISTINCT {column['column_name']} FROM feature_table_{feature.id} where \
            {column['column_name']} like '%%{value}%%'  limit 10;"
            sql = f"SELECT DISTINCT {column['column_name']} FROM feature_table_{feature.id} where \
            CAST({column['column_name']} AS VARCHAR) ILIKE '%%{value}%%'  limit 10;"
        else:
            sql = f"SELECT DISTINCT {column['column_name']} FROM feature_table_{feature.id} limit 10"
        result = feature.execute_query(sql).fetchall()
        print(result)
        d, a = {}, []
        for item in result:
            for column, value in item.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        return jsonify(results=a)

    @route('/get_records/<feature_id>', methods=('POST', 'GET',))
    @cross_origin()
    @csrf.exempt
    def fetch_records(self, feature_id):
        feature = get_feature(feature_id)

        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        sql = fetch_record_post(feature, per_page, offset)

        if "_download" in request.args and int(request.args.get("_download")):
            columns = [column['column_name'] for column in feature.columns['columns']]
            df = pd.read_sql(sql, db.engine)
            df.drop(df.columns[[0]], axis=1, inplace=True)  # df.columns is zero-based pd.Index
            df.drop(df.columns[[-1]], axis=1, inplace=True)  # df.columns is zero-based pd.Index
            df.columns = columns

            buffer = BytesIO()
            buffer.seek(0)
            df.to_excel(buffer, sheet_name='data', index=False)
            resp = make_response(buffer.getvalue())
            resp.headers[
                'Content-Disposition'] = f'attachment; filename={secure_filename(feature.subproject.title)}.xlsx'
            resp.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return resp
        else:
            result = feature.execute_query(sql)
            total_result = 0

            res = []
            columns = feature.column_keys()
            for item in result:
                data = {}
                for key, value in item.items():
                    if key == 'i_d':
                        continue
                    if key == 'total_count':
                        total_result = value
                        continue
                    data = {**data,
                            key: {"type": columns[key]['data_type']['HTML'],
                                  "name": columns[key]['original_name'],
                                  "value": value}
                            }
                res.append(dict(id=item[0], columns=data))

        return jsonify(page=page, per_page=per_page, total_result=total_result, result=res)

    @route('/<feature_id>/record/<data_id>', methods=("GET",))
    def show_feature_data(self, feature_id, data_id):

        feature: Feature = get_feature(feature_id)
        permission = feature.subproject.user_has_permission()
        if not permission or (permission and 'UPDATE' not in permission.permissions):
            return abort(403, "You don't have permission to edit this item")

        sql = f"Select * from feature_table_{feature_id} where i_d={data_id} LIMIT 1"
        result = feature.execute_query(sql).fetchone()
        if not result:
            abort(404, "Record not found")

        data = {}
        for key, value in result.items():
            if key == 'i_d':
                continue
            data = {**data,
                    key: value
                    }
        return jsonify(data)

    @route('/<feature_id>/record/<record_id>/edit', methods=('POST',))
    def edit_data(self, feature_id, record_id):
        feature: Feature = get_feature(feature_id)
        permission = feature.subproject.user_has_permission()
        if not permission or (permission and 'UPDATE' not in permission.permissions):
            return abort(403, "You don't have permission to edit this item")

        sql = f"Select * from feature_table_{feature_id} where i_d={record_id} LIMIT 1"
        result = feature.execute_query(sql).fetchone()
        if not result:
            abort(404, "Record not found")
        edit_feature_data(feature, record_id)
        return redirect(url_for('project.ProjectView:subproject', subproject_id=feature.subproject.id))

    @route('/<feature_id>/record', methods=('POST',))
    def add_data(self, feature_id):
        feature: Feature = get_feature(feature_id)
        permission = feature.subproject.user_has_permission()
        if not permission or (permission and 'CREATE' not in permission.permissions):
            return abort(403, "You don't have permission to add data to this item")

        insert_feature_data(feature)
        return redirect(url_for('project.ProjectView:subproject', subproject_id=feature.subproject.id))

    @route('/<feature_id>/record/<record_id>/delete', methods=('POST',))
    def delete_record(self, feature_id: int, record_id: int):
        feature = get_feature(feature_id)
        permission = feature.subproject.user_has_permission()
        if not permission or (permission and 'DELETE' not in permission.permissions):
            return abort(403, "You don't have permission to delete data from this item")
        feature.delete_record(record_id)
        return redirect(url_for('project.ProjectView:subproject', subproject_id=feature.subproject.id))
