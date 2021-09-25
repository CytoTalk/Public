from flask import Blueprint

from app.views.monthly_plan import MonthlyPlanView

monthly_plan = Blueprint('monthly_plans', __name__, )
MonthlyPlanView.register(monthly_plan, trailing_slash=False)
