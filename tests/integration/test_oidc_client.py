from urllib.parse import quote

from flask import url_for
import pytest
import requests


class WhenActingAsAnOIDCClient(object):

    def it_follows_the_authorization_code_flow(self, provider, client):
        assert provider.openid_configuration.called

        response = client.get(url_for('broker.auth'))
        assert response.status_code == 302

        response = requests.get(response.location, allow_redirects=False)
        assert provider.authorization_endpoint.called

        response = client.get(response.headers['location'])
        assert provider.token_endpoint.called
        assert provider.userinfo_endpoint.called

    def it_passes_an_idp_hint(self, provider, client):

        with client.session_transaction() as session:
            session['idp_hint'] = 'test-idp'

        response = client.get(url_for('broker.auth'))

        assert 'kc_idp_hint=test-idp' in response.location

    def it_passes_a_login_hint(self, provider, client):

        email = 'test@example.com'

        with client.session_transaction() as session:
            session['email_address'] = email

        response = client.get(url_for('broker.auth'))

        login_hint = 'login_hint={email}'.format(email=quote(email))
        assert login_hint in response.location

    @pytest.mark.skip
    def it_ends_the_provider_session_on_logout(self, provider, client):
        client.get(url_for('oidc_provider.logout'))
        assert provider.end_session_endpoint.called
