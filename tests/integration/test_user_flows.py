from urllib.parse import quote_plus as q_plus, urlparse

from bs4 import BeautifulSoup
from flask import request as req, session, url_for
import pytest

cookie_name = 'gateway_idp'
idp_value = 'gds-google'
department = "Government Digital Service"


def request(url, method, redirects=True):
    r = method(url, follow_redirects=redirects)
    r.soup = BeautifulSoup(r.get_data(as_text=True), 'html.parser')
    return r


class WhenOnToIDPInterstitialWithSuggestedIDPSessionSet(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, client):
        with client.session_transaction() as session:
            session['suggested_idp'] = idp_value
        self.response = request(url_for('main.to_idp'), client.get)

    def it_stores_suggested_IDP_in_Gateway_IDP_cookie(self):
        cookie = self.response.headers['Set-Cookie']
        assert "{}={};".format(cookie_name, idp_value) in cookie


class WhenNavigatingToGatewayWithGatewayIDPCookieSet(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, client):
        client.set_cookie('localhost', cookie_name, idp_value)
        self.response = request(
            url_for('main.authentication_request'), client.get)

    def it_redirects_to_department_confirmation_with_department_set(self):
        assert url_for('main.confirm_dept') in req.url
        assert department in self.response.soup.select_one("form legend").text

    def it_redirects_to_dept_confirm_and_does_not_show_email_given_box(self):
        assert url_for('main.confirm_dept') in req.url
        assert self.response.soup.select_one(".email-given") is None


class WhenNavigatingToGatewayAfterBeingProxied(object):
    client_id = 'test'
    redirect_uri = 'https://test'
    px = 'https://proxy/auth'

    @pytest.fixture(autouse=True)
    def setup_page(self, client):
        self.response = request(
            url_for(
                'main.authentication_request',
                client_id=self.client_id,
                redirect_uri=self.redirect_uri,
                px=self.px),
            client.get)

    def it_has_px_q_and_px_url_sessions_set(self):
        assert self.px == session['px_url']
        assert 'client_id={}'.format(self.client_id) in session['px_q']
        assert 'redirect_uri={}'.format(
            q_plus(self.redirect_uri)) in session['px_q']

    def it_will_redirect_to_broker_with_idp_hint_in_query_string(self, client):
        with client.session_transaction() as session:
            session['suggested_idp'] = idp_value

        self.response = request(url_for('main.to_idp'), client.get)
        self.response = request(
            url_for('broker.auth'), client.get, redirects=False)

        assert self.response.location.startswith(self.px)

        query = urlparse(self.response.location).query

        assert 'client_id={}'.format(self.client_id) in query
        assert 'redirect_uri={}'.format(q_plus(self.redirect_uri)) in query
        assert 'kc_idp_hint={}'.format(idp_value) in query
