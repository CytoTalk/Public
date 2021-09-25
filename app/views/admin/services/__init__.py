from cloudinary.uploader import upload, destroy
from flask import render_template, request, flash, redirect, url_for
from flask_classful import FlaskView, route
from flask_login import login_required
from slugify import slugify

from app.forms.admin.service import ServiceForm
from app.models.Service import Service, ServiceImage


def get_service(service_id: int) -> Service:
    return Service.query.get(service_id)


def unique_slug(text, service=None) -> str:
    slug = slugify(text)
    query = Service.query.filter(Service.slug == slug)
    if service:
        query.filter(Service.id != service.id)
    res = query.all()
    if not res:
        return slug
    return slug + f"-{len(res)}"


class ServiceView(FlaskView):
    decorators = [login_required]

    def index(self):
        services = Service.query.all()
        return render_template('admin/service/index.html', services=services)

    @route('/create', methods=['GET', 'POST'])
    def create(self):
        form = ServiceForm()
        if form.validate_on_submit():
            service = Service.query.filter_by(title=form.title.data).first()
            if service:
                flash("A service with the title already exist", 'error')
                return redirect(request.url)

            service = Service(
                long_description=form.long_description.data,
                short_description=form.short_description.data,
                title=form.title.data,
                price=form.price.data,
                slug=unique_slug(form.title.data)
            )
            service.save()

            try:
                main_picture_upload = upload(form.main_picture.data)
                ServiceImage(
                    public_id=main_picture_upload['public_id'],
                    url=main_picture_upload['secure_url'],
                    is_main_picture=True,
                    service_id=service.id
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
                        ServiceImage(
                            public_id=image['public_id'],
                            url=image['secure_url'],
                            is_main_picture=False,
                            service_id=service.id
                        ).save()
            flash("Service was created successfully", 'success')
            return redirect(url_for('admin.ServiceView:index'))
        else:
            return render_template('admin/service/create.html', form=form)

    @route('/<service_id>/update', methods=('GET', 'POST',))
    def update(self, service_id):
        service = get_service(service_id)
        form = ServiceForm(long_description=service.long_description,
                           short_description=service.short_description, price=service.price,
                           title=service.title)
        if request.method == 'POST':
            service.long_description = form.long_description.data
            service.short_description = form.short_description.data
            service.title = form.title.data
            service.price = form.price.data
            service.slug = unique_slug(form.title.data, service)
            service.save()
            images_to_delete = request.form.getlist('images_to_delete')
            if images_to_delete:
                for image in images_to_delete:
                    destroy(image)
                    result = ServiceImage.query.filter_by(public_id=image).first()
                    if result:
                        result.delete()
            if form.main_picture.data:

                try:
                    main_picture_upload = upload(form.main_picture.data)

                    query = ServiceImage.query.filter_by(is_main_picture=True, service_id=service.id).first()
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
                        ServiceImage(
                            public_id=image['public_id'],
                            url=image['secure_url'],
                            is_main_picture=False,
                            service_id=service.id
                        ).save()
            flash("Service was updated successfully", "success")

            return redirect(url_for("admin.ServiceView:index"))
        return render_template('admin/service/edit.html', form=form, service=service)

    @route('/<service_id>', methods=('GET',))
    def show(self, service_id):
        service = get_service(service_id)
        return render_template('admin/service/show.html', service=service)

    @route('<service_id>/delete', methods=('POST',))
    def delete(self, service_id):
        service = get_service(service_id)
        service.delete()
        flash("Service was deleted successfully", 'success')
        return redirect(url_for('admin.ServiceView:index'))
