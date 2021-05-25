from pathlib import Path

import sqlalchemy
from flask import send_from_directory, current_app, jsonify, abort
from flask import request, render_template
from flask_classful import FlaskView, route
from flask_cors import cross_origin
from flask_login import current_user
from sqlalchemy import text
from app import db, csrf
from app.models.Feature import Feature
from app.views.admin.feature import get_feature


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
        if request.method == 'GET':
            sql = text(f"select * from feature_table_{feature_id} limit 10")
        else:
            conditions = []
            for key, value in request.form.items():
                column = feature.get_column_data(key.replace('[]', ''))
                if column['data_type']['HTML'] == 'number':
                    values = sorted(request.form.getlist(key))
                    try:
                        low = values[0]
                        high = values[1]
                    except IndexError:
                        low = 0
                        high = 0
                    if column['data_type']['PYTHON'] == 'int':
                        statement = f"({key.replace('[]', '')}::integer between {low} and {high})"
                    else:
                        statement = f"({key.replace('[]', '')}::float between {low} and {high})"

                elif column['data_type']['HTML'] == 'checkbox':
                    if value != 'all':
                        statement = f"{column['column_name']} ={value}"
                else:
                    statement = f"({key}::text like '%{value}%')"
                conditions.append(statement)
            params = " and ".join(conditions)
            sql = text(
                f"select * from feature_table_{feature_id} where {params} limit 10")
            print(sql)
        result = feature.execute_query(sql)

        res = []
        columns = feature.column_keys()
        for item in result:
            data = {}
            for key, value in item.items():
                if key == 'i_d':
                    continue
                data = {**data,
                        key: {"type": columns[key]['data_type']['HTML'],
                              "name": columns[key]['original_name'],
                              "value": value}
                        }
            res.append(data)

        return jsonify(result=res)
