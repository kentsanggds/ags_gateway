import mock

from flask import redirect as flask_redirect, session, url_for
import pytest
import requests

from tests.oidc_testbed import MockOIDCClient


@pytest.yield_fixture
def skip_idp_interstitial(client):

    with mock.patch('app.main.views.auth.redirect') as redirect:

        def skip_interstitial(url, *args, **kwargs):

            if url == url_for('main.to_idp'):
                idp = session.get('suggested_idp')
                url = url_for('broker.auth', idp_hint=idp)

            return flask_redirect(url, *args, **kwargs)

        redirect.side_effect = skip_interstitial

        yield redirect


@pytest.yield_fixture
def skip_service_interstitial(client):

    with mock.patch('app.broker.redirect') as redirect:

        def skip_interstitial(url, *args, **kwargs):

            if url == url_for('main.to_service'):
                url = session.get('auth_redirect')

            return flask_redirect(url, *args, **kwargs)

        redirect.side_effect = skip_interstitial

        yield redirect


@pytest.yield_fixture
def oidc_rp(
        responses, app, client, skip_idp_interstitial,
        skip_service_interstitial):

    issuer = url_for('main.index', _external=True)
    with MockOIDCClient(responses, issuer, client) as rp:
        yield rp


class TestOIDCProvider(object):

    def test_handle_provider_config(self, oidc_rp, client):
        response = client.get(url_for('oidc_provider.provider_config'))
        assert response.status_code == 200
        assert 'authorization_endpoint' in response.json

    def test_handle_authorization_request(self, oidc_rp, client):
        response = client.get(oidc_rp.auth_request(), follow_redirects=True)
        assert response.status_code == 200
        assert 'Do you know your work email' in response.get_data(as_text=True)

    def test_make_callback(self, oidc_rp, client):

        # client request authentication
        response = client.get(oidc_rp.auth_request(), follow_redirects=True)

        # authenticate with broker
        response = client.get(url_for('broker.auth', idp_hint='test-idp'))
        response = requests.get(response.location, allow_redirects=False)
        response = client.get(response.headers['location'])

        # redirect to client callback
        response = client.get(url_for('broker.auth', idp_hint='test-idp'))
        assert response.status_code == 302
        assert 'code=' in response.location

    def test_handle_token_and_userinfo_request(self, oidc_rp, client, app):

        # client request authentication
        response = client.get(oidc_rp.auth_request(), follow_redirects=True)

        # authenticate with broker
        response = client.get(url_for('broker.auth', idp_hint='test-idp'))
        response = requests.get(response.location, allow_redirects=False)
        response = client.get(response.headers['location'])

        # redirect to client callback
        response = client.get(url_for('broker.auth', idp_hint='test-idp'))
        code, state = oidc_rp.parse_auth_response(response.location)

        # exchange code for token
        response = oidc_rp.token_request(code, state)
        assert 'access_token' in response
        assert 'id_token' in response

        # request userinfo
        userinfo = oidc_rp.userinfo_request(response['id_token'], state)
        assert 'email' in userinfo

    @pytest.mark.xfail
    def test_invalid_provider_token_request(self):
        assert False

    @pytest.mark.xfail
    def test_oath_error_provider_token_request(self):
        assert False

    @pytest.mark.xfail
    def test_handle_userinfo_request(self):
        assert False

    @pytest.mark.xfail
    def test_userinfo_requested_claims(self):
        assert False

    @pytest.mark.xfail
    def test_handle_end_session_request(self):
        assert False
