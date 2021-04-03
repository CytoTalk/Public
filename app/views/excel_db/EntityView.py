from flask_classful import FlaskView, route

from app.functions.ExcelDatabase import ExcelDatabase
from flask import jsonify, request
from app.functions.store_excel import HandleExcel


class EntityView(FlaskView):
    def get(self):
        exc = ExcelDatabase('/home/lennox/Desktop/work/flask-ai/assets/locations.xlsx')
        query_list = []
        for param in request.args.items():
            query_list.append(f"{param[0]}=='{param[1]}'")
        query = " & ".join(query_list)
        result = exc.query(query)
        return jsonify(result)
