from flask import Blueprint, current_app, redirect, session, url_for


broker = Blueprint('broker', __name__)


@broker.route('/broker')
def auth():
    return redirect('https://gateway.civilservice.digital/idp-auth{}'.format(session['kc_q']))
