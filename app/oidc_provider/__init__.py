from flask import Blueprint, url_for
from jwkest.jwk import RSAKey, rsa_load
from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.subject_identifier import HashBasedSubjectIdentifierFactory

from app.oidc_provider.userinfo import Userinfo


oidc_provider = Blueprint('oidc_provider', __name__)  # noqa


from app.oidc_provider import views  # noqa


def init_oidc_provider(app):
    with app.app_context():
        config = {
            'issuer': app.config['OIDC_PROVIDER']['issuer'],
            'authorization_endpoint': url_for('oidc_provider.auth'),
            'jwks_uri': url_for('oidc_provider.jwks'),
            'token_endpoint': url_for('oidc_provider.token'),
            'userinfo_endpoint': url_for('oidc_provider.userinfo'),
            'registration_endpoint': url_for('oidc_provider.register'),
            'end_session_endpoint': url_for('oidc_provider.logout'),
            'scopes_supported': ['openid', 'profile'],
            'response_types_supported': [
                'code', 'code id_token', 'code token', 'code id_token token'],
            'response_modes_supported': ['query', 'fragment'],
            'grant_types_supported': ['authorization_code', 'implicit'],
            'subject_types_supported': ['pairwise'],
            'token_endpoint_auth_methods_supported': ['client_secret_basic'],
            'claims_parameter_supported': True
        }
    userinfo_db = Userinfo()
    signing_key = RSAKey(key=rsa_load('signing_key.pem'), alg='RS256')
    authz_state = AuthorizationState(HashBasedSubjectIdentifierFactory(
        app.config['OIDC_PROVIDER']['subject_id_hash_salt']))
    clients = {
        'notify-test': {
            'client_name': 'GOV.UK Notify',
            'redirect_uris': [
                'http://localhost:6012/oidc_callback',
            ],
            'response_types': [
                'code',
            ],
        },
    }
    provider = Provider(signing_key, config, authz_state, clients, userinfo_db)
    return provider
