from flask import render_template
from flask_classful import FlaskView, route

from app.models.MonthlyPlan import MonthlyPlan


class MonthlyPlanView(FlaskView):
    """
    This is where editing begins
    """

    @route('/', methods=('GET',))
    def index(self):
        monthly_plans = MonthlyPlan.query.all()

        return render_template('front/monthly_plan/index.html', monthly_plans=monthly_plans)

    @route('/<monthly_plan_slug>', methods=('GET',))
    def show(self, monthly_plan_slug):
        monthly_plan = MonthlyPlan.query.filter_by(slug=monthly_plan_slug).first_or_404()
        return render_template(
            'front/monthly_plan/show.html', monthly_plan=monthly_plan)
