from flask_login import login_required

from app.admin import admin
from flask import render_template


@admin.route('/dashboard', methods=('GET',))
@login_required
def dashboard():
    return render_template('admin/dashboard.html')
