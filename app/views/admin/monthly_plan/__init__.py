from cloudinary.uploader import upload, destroy
from flask import render_template, request, flash, redirect, url_for
from flask_classful import FlaskView, route
from flask_login import login_required
from slugify import slugify

from app.forms.admin.monthly_plan import MonthlyPlanForm
from app.models.MonthlyPlan import MonthlyPlan, MonthlyPlanImage


def get_monthly_plan(monthly_plan_id: int) -> MonthlyPlan:
    return MonthlyPlan.query.get(monthly_plan_id)


def unique_slug(text, monthly_plan=None) -> str:
    slug = slugify(text)
    query = MonthlyPlan.query.filter(MonthlyPlan.slug == slug)
    if monthly_plan:
        query.filter(MonthlyPlan.id != monthly_plan.id)
    res = query.all()
    if not res:
        return slug
    return slug + f"-{len(res)}"


class MonthlyPlanView(FlaskView):
    decorators = [login_required]

    def index(self):
        monthly_plans = MonthlyPlan.query.all()
        return render_template('admin/monthly_plan/index.html', monthly_plans=monthly_plans)

    @route('/create', methods=['GET', 'POST'])
    def create(self):
        form = MonthlyPlanForm()
        if form.validate_on_submit():
            monthly_plan = MonthlyPlan.query.filter_by(title=form.title.data).first()
            if monthly_plan:
                flash("A monthly_plan with the title already exist", 'error')
                return redirect(request.url)

            monthly_plan = MonthlyPlan(
                long_description=form.long_description.data,
                short_description=form.short_description.data,
                title=form.title.data,
                price=form.price.data,
                slug=unique_slug(form.title.data)
            )
            monthly_plan.save()

            try:
                main_picture_upload = upload(form.main_picture.data)
                MonthlyPlanImage(
                    public_id=main_picture_upload['public_id'],
                    url=main_picture_upload['secure_url'],
                    is_main_picture=True,
                    monthly_plan_id=monthly_plan.id
                ).save()
            except Exception as exception:
                flash(str(exception), 'error')
                return redirect(request.url)

            if len(form.other_images.data):
                image_bag = []

                for image in form.other_images.data:
                    try:
                        image_bag.append(upload(image))
                    except Exception as exception:
                        flash(str(exception), 'error')
                if image_bag:
                    for image in image_bag:
                        MonthlyPlanImage(
                            public_id=image['public_id'],
                            url=image['secure_url'],
                            is_main_picture=False,
                            monthly_plan_id=monthly_plan.id
                        ).save()
            flash("MonthlyPlan was created successfully", 'success')
            return redirect(url_for('admin.MonthlyPlanView:index'))
        else:
            return render_template('admin/monthly_plan/create.html', form=form)

    @route('/<monthly_plan_id>/update', methods=('GET', 'POST',))
    def update(self, monthly_plan_id):
        monthly_plan = get_monthly_plan(monthly_plan_id)
        form = MonthlyPlanForm(long_description=monthly_plan.long_description,
                               short_description=monthly_plan.short_description, price=monthly_plan.price,
                               title=monthly_plan.title)
        if request.method == 'POST':
            monthly_plan.long_description = form.long_description.data
            monthly_plan.short_description = form.short_description.data
            monthly_plan.title = form.title.data
            monthly_plan.price = form.price.data
            monthly_plan.slug = unique_slug(form.title.data, monthly_plan)
            monthly_plan.save()
            images_to_delete = request.form.getlist('images_to_delete')
            if images_to_delete:
                for image in images_to_delete:
                    destroy(image)
                    result = MonthlyPlanImage.query.filter_by(public_id=image).first()
                    if result:
                        result.delete()
            if form.main_picture.data:

                try:
                    main_picture_upload = upload(form.main_picture.data)

                    query = MonthlyPlanImage.query.filter_by(is_main_picture=True,
                                                             monthly_plan_id=monthly_plan.id).first()
                    query.public_id = main_picture_upload['public_id']
                    query.url = main_picture_upload['secure_url']
                    query.save()

                except Exception as exception:
                    flash(str(exception), 'error')
            if len(form.other_images.data):
                image_bag = []

                for image in form.other_images.data:
                    try:
                        image_bag.append(upload(image))
                    except Exception as exception:
                        flash(str(exception), 'error')
                if image_bag:
                    for image in image_bag:
                        MonthlyPlanImage(
                            public_id=image['public_id'],
                            url=image['secure_url'],
                            is_main_picture=False,
                            monthly_plan_id=monthly_plan.id
                        ).save()
            flash("MonthlyPlan was updated successfully", "success")

            return redirect(url_for("admin.MonthlyPlanView:index"))
        return render_template('admin/monthly_plan/edit.html', form=form, monthly_plan=monthly_plan)

    @route('/<monthly_plan_id>', methods=('GET',))
    def show(self, monthly_plan_id):
        monthly_plan = get_monthly_plan(monthly_plan_id)
        return render_template('admin/monthly_plan/show.html', monthly_plan=monthly_plan)

    @route('<monthly_plan_id>/delete', methods=('POST',))
    def delete(self, monthly_plan_id):
        monthly_plan = get_monthly_plan(monthly_plan_id)
        monthly_plan.delete()
        flash("MonthlyPlan was deleted successfully", 'success')
        return redirect(url_for('admin.MonthlyPlanView:index'))
