from flask import Blueprint, redirect

from app.oidc_client.decorators import authenticate
from app.oidc_provider.views import authorize


broker = Blueprint('broker', __name__)


@broker.route('/broker')
@authenticate
def auth():
    return redirect(authorize())
