import json
from urllib.parse import urlencode
from flask import url_for, request
import mock
import pytest

from oic.oic import AuthorizationRequest, AccessTokenResponse


class TestOIDCProvider(object):

    @mock.patch('pyop.provider.Provider.parse_authentication_request')
    def test_handle_auth_request(self, mock_parse_authentication_request,
                                 app_, client, request_params,
                                 request_headers):

        mock_parse_authentication_request.return_value = \
            AuthorizationRequest().deserialize(urlencode(request_params))

        resp = client.get(url_for('oidc_provider.auth', **request_params),
                          headers=request_headers)

        mock_parse_authentication_request.assert_called_once_with(
            urlencode(request_params),
            request.headers)

        assert resp.status_code == 302
        assert resp.location.endswith(url_for('main.authentication_request'))

    @mock.patch('pyop.provider.Provider.handle_token_request')
    def test_handle_token_request(self, mock_handle_token_request, app_,
                                  client, request_params, request_headers,
                                  token_response):

        mock_handle_token_request.return_value = \
            AccessTokenResponse().deserialize(urlencode(token_response))

        resp = client.post(url_for('oidc_provider.token'),
                           data=urlencode(request_params),
                           headers=request_headers)

        mock_handle_token_request.assert_called_once_with(
            urlencode(request_params),
            request.headers)

        assert resp.status_code == 200
        assert resp.mimetype == 'application/json'
        assert json.loads(resp.get_data(as_text=True)) == token_response

    @pytest.mark.xfail
    def test_handle_userinfo_request(self):
        assert False

    @pytest.mark.xfail
    def test_userinfo_requested_claims(self):
        assert False

    @pytest.mark.xfail
    def test_handle_end_session_request(self):
        assert False
