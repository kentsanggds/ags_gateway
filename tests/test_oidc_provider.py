from flask import url_for, request
import mock
import pytest

from oic.oic import AuthorizationRequest


class TestOIDCProvider(object):

    @mock.patch('pyop.provider.Provider.parse_authentication_request')
    def test_handle_auth_request(self, mock_parse_authentication_request,
                                 app_, client):
        request_params = {
            'param': 'mock',
        }

        request_headers = {
            'Content-Length': '0',
            'Host': app_.config['SERVER_NAME'],
            'Content-Type': '',
        }

        mock_parse_authentication_request.return_value = \
            AuthorizationRequest().deserialize('param=mock')

        resp = client.get(url_for('oidc_provider.auth', **request_params),
                          headers=request_headers)

        mock_parse_authentication_request.assert_called_once_with(
            'param=mock',
            request.headers)

        assert resp.status_code == 302
        assert resp.location.endswith(url_for('main.authentication_request'))

    @pytest.mark.xfail
    def test_handle_token_request(self):
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
