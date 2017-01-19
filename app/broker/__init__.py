from flask import Blueprint, current_app, redirect, session, url_for

from app.oidc_client.decorators import authenticate
from app.oidc_provider.views import authorize


broker = Blueprint('broker', __name__)


@broker.route('/broker')
@authenticate
def auth():
    session['auth_redirect'] = authorize()

    if current_app.config.get('DISABLE_INTERSTITIALS'):
        return redirect(session['auth_redirect'])

    return redirect(url_for('main.to_service'))
