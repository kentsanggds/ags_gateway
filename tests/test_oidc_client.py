from flask import session, url_for
import mock
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

    @pytest.mark.xfail
    def test_send_token_request(self):
        assert False

    @pytest.mark.xfail
    def test_send_userinfo_request(self):
        assert False

    @pytest.mark.xfail
    def test_send_logout_request(self):
        assert False
