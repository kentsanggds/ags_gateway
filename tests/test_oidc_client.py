from flask import session, url_for
import mock
from oic.oic import AuthnToken
import pytest


class TestOIDCClient(object):

    @mock.patch('oic.oic.Client.construct_AuthorizationRequest')
    def test_send_authentication_request(self, mock_auth_request, app_,
                                         client):
        callback_url = url_for('oidc_callback', _external=True)

        with client.session_transaction() as sess:
            sess['idp_hint'] = 'mock_idp_hint'
            sess['email_address'] = 'mock_email_address'

        resp = client.get(url_for('broker.auth'))

        mock_auth_request.assert_called_once_with(request_args={
            'client_id': app_.config['OIDC_CLIENT']['client_id'],
            'response_type': 'code',
            'scope': ['openid', 'profile'],
            'redirect_uri': callback_url,
            'state': session['state'],
            'nonce': session['nonce'],
            'kc_idp_hint': 'mock_idp_hint',
            'login_hint': 'mock_email_address',
            'claims': {
                'userinfo': {
                    'email': {'essential': True},
                    'name': {'essential': True}
                }
            }
        })

        assert resp.status_code == 302

    @mock.patch('app.oidc_client.views._get_userinfo')
    @mock.patch('oic.oic.Client.parse_response')
    @mock.patch('oic.oic.Client.do_access_token_request')
    def test_send_token_request(self, do_access_token_request,
                                mock_parse_response, mocked_get_userinfo,
                                app_, client):
        callback_url = url_for('oidc_callback', _external=True)

        mock_parse_response.return_value = {
            'state': 'mocked_state',
            'code': 'mocked_code',
        }

        do_access_token_request.return_value = {
            'id_token': AuthnToken(nonce='mocked_nonce', sub='mocked_sub'),
            'access_token': 'mocked_access_token',
        }

        with client.session_transaction() as sess:
            sess['state'] = 'mocked_state'
            sess['nonce'] = 'mocked_nonce'
            sess['destination'] = '/mocked_destination'

        resp = client.get(url_for('oidc_callback'))

        do_access_token_request.assert_called_once_with(
            authn_method='client_secret_basic',
            request_args={
                'redirect_uri': callback_url,
                'code': 'mocked_code'},
            state='mocked_state')

        assert resp.status_code == 302
        assert resp.location.endswith('/mocked_destination')

    @pytest.mark.xfail
    def test_send_userinfo_request(self):
        assert False

    @pytest.mark.xfail
    def test_send_logout_request(self):
        assert False
