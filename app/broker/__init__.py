from flask import Blueprint, current_app, redirect, session, url_for, request


broker = Blueprint('broker', __name__)


@broker.route('/broker')
def auth():
    return redirect('{}?{}'.format(session['px_url'], session['px_q']))
