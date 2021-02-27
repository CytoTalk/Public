from flask import render_template

from app.main import main


@main.route('/')
def homepage():
    return render_template('main/index.html')
