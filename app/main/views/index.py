from flask import render_template

from app.main import main


@main.route('/')
def index():
    return render_template('views/index_signed_out.html')
