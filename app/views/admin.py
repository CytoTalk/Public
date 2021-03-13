from flask_login import login_required

from app.admin import admin
from flask import render_template, request, redirect, url_for
from ..models import Posts


@admin.route('/dashboard', methods=('GET', ))
@login_required
def dashboard():

    return render_template('admin/dashboard.html')

@admin.route('/upload', methods=('POST', 'GET'))
def uploaded_file():
    if request.method =='POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename !='':
            uploaded_file.save(uploaded_file.filename)
        return redirect(url_for('main.projects'))
    return render_template('admin/upload_form.html')

