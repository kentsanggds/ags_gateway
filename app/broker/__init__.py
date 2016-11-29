from flask import Blueprint, jsonify, session

from app.oidc_client.decorators import authenticate


broker = Blueprint('broker', __name__)


@broker.route('/broker')
@authenticate
def auth():
    return jsonify(dict(session))
