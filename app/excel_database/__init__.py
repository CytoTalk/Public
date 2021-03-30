from flask import Blueprint
from app.views.excel_db import EntityView
excel_db = Blueprint('edb',__name__,url_prefix='/excel_db')

EntityView.EntityView.register(excel_db, trailing_slash=False)
