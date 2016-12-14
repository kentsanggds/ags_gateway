# -*- coding: utf-8 -*-
import requests
from urllib.parse import unquote, urlencode

from flask import (
    current_app,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
    json,
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


def authorize():
    id_token = session['id_token']
    auth_request = AuthorizationRequest(**session['auth_request'])
    auth_response = current_app.provider.authorize(
        auth_request,
        id_token['sub'])

    return auth_response.request(
        auth_request['redirect_uri'],
        # url_for('main.to_service'),
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
    token = current_app.provider.handle_token_request(
        request.get_data().decode('utf-8'),
        request.headers
    ).to_dict()

    return token


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
    current_app.logger.info('Requesting userinfo')

    data = current_app.provider.handle_userinfo_request(
        request.get_data().decode('utf-8'),
        request.headers
    ).to_dict()

    return data


def userinfo_error(exception):
    error_response = UserInfoErrorResponse(
        error='invalid_token', error_description=str(exception))

    response = make_response((jsonify(error_response.to_dict()), 401))
    response.headers['WWW-Authenticate'] = AccessToken.BEARER_TOKEN_TYPE

    return response


# @op.route('/oidc/logout', methods=['GET', 'POST'])
# def logout():
#     if request.method == 'POST':

#         if 'logout' in request.form:
#             return do_logout()

#         return make_response('You chose not to logout')

#     session['end_session_request'] = request.args

#     return render_template('views/oidc_provider/logout.html')


@op.route('/logout-info', methods=['GET', 'POST'])
def logout_info():

    return render_template('views/logout_info.html', next_url=session['logout_redirect'])


@op.route('/oidc/logout', methods=['GET', 'POST'])
# def do_logout():
def logout():

    end_session_request = EndSessionRequest().deserialize(urlencode(request.args))

    session['end_session_request'] = end_session_request.to_dict()

    try:
        redirect_url = logout_user()

    except InvalidSubjectIdentifier as error:
        raise BadRequest('Logout unsuccessful')

    return render_template('views/logout_info.html', next_url=redirect_url)


def logout_user():
    params = session['end_session_request']

    print("logout_user:{}".format(params))

    params.update({'id_token_hint': session['id_token_jwt']})

    print("logout_user2:{}".format(params))

    request = EndSessionRequest().from_dict(params)

    current_app.provider.logout_user(end_session_request=request)

    return current_app.provider.do_post_logout_redirect(request)
