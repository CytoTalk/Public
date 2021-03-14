from flask_login import login_required
from flask import app
from hashlib import md5
from app.admin import admin
from flask import Flask, render_template, request, redirect, url_for, g
import time
import os
import config
from pathlib import Path
import sqlalchemy



# 'ALLOWED_EXTENSIONS':  app.config['ALLOWED_EXTENSIONS']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
PROJECT_PATH = Path(__file__).parent.parent
UPLOAD_FOLDER = Path.joinpath(PROJECT_PATH, 'uploads')
OUTPUT_PATH = Path.joinpath(PROJECT_PATH, 'output_location')
ASSETS_PATH = Path.joinpath(PROJECT_PATH, 'assets')
BASE_DIR           = '/var/www/flaskgur/'
DATABASE           = BASE_DIR + 'flaskgur.db'

app = Flask(__name__)
app.config.from_object(__name__)


@admin.route('/dashboard', methods=('GET', ))
@login_required
def dashboard():

    return render_template('admin/dashboard.html')

# @admin.route('/upload', methods=('POST', 'GET'))
# def uploaded_file():
#     if request.method =='POST':
#         uploaded_file = request.files['file']
#         if uploaded_file.filename !='':
#             uploaded_file.save(uploaded_file.filename)
#         return redirect(url_for('main.projects'))
#     return render_template('admin/upload_form.html')

# Make sure extension is in the ALLOWD_EXTENSIONS set
def connect_db():
    return sqlalchemy.connect(app.config['DATABASE'])


def check_extension(extension):
    return extension in ALLOWED_EXTENSIONS


# Insert filename and category into database
def add_pic(filename, category, project):
    g.db.execute('insert into pics (filename, category, project) values (?, ?, ?)', [filename, category, project])
    g.db.commit()


@admin.before_request
def before_request():
    g.db = connect_db()

@admin.route('/upload', methods=('POST', 'GET'))
def upload_pic():
    if request.method == 'POST':
        file = request.files['file']
        category = request.form['category']
        project = request.form['project']

        try:
            extension = file.filename.rsplit('.', 1)[1].lower()
        except IndexError as error:
            abort(404)
        if file and check_extension(extension):
            # Salt and hash the file contents
            filename = md5(file.read() + bytes(str(round(time.time() * 1000)), 'utf-8')).hexdigest() + '.' + extension
            file.seek(0)  # Move cursor back to beginning so we can write to disk
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            add_pic(filename, category, project)
            gen_thumbnail(filename)
            return redirect(url_for('main.projects', filename=filename))
        else:
            # Bad file extension
            abort(404)
    else:
        return render_template('admin/upload_form.html') 

