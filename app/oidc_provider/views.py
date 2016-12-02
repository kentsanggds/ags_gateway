# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from flask import (
    current_app,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from oic.oic.message import (
    AuthorizationRequest,
    EndSessionRequest,
    TokenErrorResponse,
    UserInfoErrorResponse,
)
from pyop.access_token import AccessToken
from pyop.exceptions import (
    BearerTokenError,
    InvalidAccessToken,
    InvalidAuthenticationRequest,
    InvalidClientAuthentication,
    InvalidClientRegistrationRequest,
    InvalidSubjectIdentifier,
    OAuthError,
)
from pyop.util import should_fragment_encode
from werkzeug.exceptions import BadRequest

from app.oidc_provider import oidc_provider as op


@op.route('/oidc/registration', methods=['POST'])
def register():
    try:
        client_metadata = register_client()

    except InvalidClientRegistrationRequest as error:
        return make_response((jsonify(error.to_dict()), 400))

    return make_response((jsonify(client_metadata), 201))


def register_client():
    return current_app.provider.handle_client_registration_request(
        request.get_data().decode('utf-8')).to_dict()


@op.route('/oidc/auth', methods=['GET'])
def auth():
    try:
        auth_request = parse_auth_request()

    except InvalidAuthenticationRequest as error:
        callback_url = error.to_error_url()

        if callback_url:
            return redirect(callback_url, 303)

        raise BadRequest('Something went wrong: {}'.format(str(error)))

    session['auth_request'] = auth_request.to_dict()

    return redirect(url_for('main.authentication_request'))


def parse_auth_request():
    return current_app.provider.parse_authentication_request(
        urlencode(request.args), request.headers)


def authorize(user):
    auth_request = AuthorizationRequest(**session['auth_request'])
    auth_response = current_app.provider.authorize(auth_request, user)
    return auth_response.request(
        auth_request['redirect_uri'],
        should_fragment_encode(auth_request))


@op.route('/.well-known/openid-configuration')
def provider_config():
    return jsonify(current_app.provider.provider_configuration.to_dict())


@op.route('/oidc/keys')
def jwks():
    return jsonify(current_app.provider.jwks)


@op.route('/oidc/token', methods=['POST'])
def token():
    try:
        return jsonify(access_token())

    except (InvalidClientAuthentication, OAuthError) as e:
        return token_error(e)


def access_token():
    current_app.logger.debug(
        'TOKEN REQUEST:\n{}{}'.format(request.headers, request.get_data()))

    return current_app.provider.handle_token_request(
        request.get_data().decode('utf-8'),
        request.headers
    ).to_dict()


def token_error(exception):

    error_response = TokenErrorResponse(
        error=exception.oauth_error, error_description=str(exception))

    response = make_response((jsonify(error_response.to_dict()), 400))

    if isinstance(exception, InvalidClientAuthentication):
        response.status = '401'
        response.headers['WWW-Authenticate'] = 'basic'

    return response


@op.route('/oidc/userinfo', methods=['GET', 'POST'])
def userinfo():
    try:
        return jsonify(userinfo_data())

    except (BearerTokenError, InvalidAccessToken) as e:
        return userinfo_error(e)


def userinfo_data():
    return current_app.provider.handle_userinfo_request(
        request.get_data().decode('utf-8'),
        request.headers
    ).to_dict()


def userinfo_error(exception):
    error_response = UserInfoErrorResponse(
        error='invalid_token', error_description=str(exception))

    response = make_response((jsonify(error_response.to_dict()), 401))
    response.headers['WWW-Authenticate'] = AccessToken.BEARER_TOKEN_TYPE

    return response


@op.route('/oidc/logout', methods=['GET', 'POST'])
def logout():

    if request.method == 'POST':

        if 'logout' in request.form:
            return do_logout()

        return make_response('You chose not to logout')

    session['end_session_request'] = urlencode(request.args)

    return render_template('views/oidc_provider/logout.html')


def do_logout():

    try:
        redirect_url = logout_user()

    except InvalidSubjectIdentifier as error:
        raise BadRequest('Logout unsuccessful')

    if redirect_url:
        return redirect(redirect_url, 303)

    return make_response('Logout successful')


def logout_user():
    request = EndSessionRequest().deserialize(session['end_session_request'])

    current_app.provider.logout_user(request)

    return current_app.provider.do_post_logout_redirect(request)
