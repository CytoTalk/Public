from flask import render_template, request, flash, redirect, url_for
from flask_classful import FlaskView, route
from flask_login import login_required, current_user

from app.forms.admin.user import UserForm
from app.models.User import User


def get_user(user_id: int) -> User:
    return User.query.filter_by(id=user_id).first_or_404()


class UserView(FlaskView):
    decorators = [login_required]

    def index(self):
        users = User.query.filter(User.id != current_user.id)
        return render_template('admin/user/index.html', users=users)

    @route('/create', methods=['GET', 'POST'])
    def create(self):
        form = UserForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("Email already exist, please use another email!", 'error')
                return redirect(request.url)
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                is_active=form.is_active.data
                # password=hash_password(form.password.data)
            )
            user.create()
            flash("Account was created successfully", 'success')
            return redirect(url_for('admin.UserView:index'))
        else:
            return render_template('admin/user/create.html', form=form)

    @route('/<user_id>/update', methods=('GET', 'POST',))
    def update(self, user_id):
        user = get_user(user_id)
        form = UserForm(first_name=user.first_name, last_name=user.last_name, email=user.email,
                        password=user.password, is_active=user.is_active)
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.password = form.password.data
            user.is_active = form.is_active.data
            user.save()
            flash("User was updated successfully", "success")
            return redirect(url_for("admin.UserView:index"))
        return render_template('admin/user/edit.html', form=form, user_id=user_id)
    
    @route('/<user_id>', methods=('GET',))
    def show(self, user_id):
        user = get_user(user_id)
        return render_template('admin/user/show.html', user=user)

    @route('<user_id>/delete', methods=('POST',))
    def delete(self, user_id):
        user = get_user(user_id)
        user.delete()
        flash("User was deleted successfully", 'success')
        return redirect(url_for('admin.UserView:index'))
