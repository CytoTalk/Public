from flask import Blueprint

from app.views.feature import FeatureView

feature = Blueprint('feature', __name__, url_prefix='/feature')
FeatureView.register(feature, trailing_slash=False)
