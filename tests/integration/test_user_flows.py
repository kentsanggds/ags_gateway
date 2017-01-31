from bs4 import BeautifulSoup
from flask import url_for
import pytest


def req(url, method, **kwargs):
    r = method(url, **kwargs)
    r.soup = BeautifulSoup(r.get_data(as_text=True), 'html.parser')
    return r


cookie = {'name': 'gateway_idp', 'value': 'gds-google'}
department = "Government Digital Service"


class WhenOnToIDPInterstitial(object):

    @pytest.mark.xfail
    def it_sets_Gateway_IDP_cookie_to_suggested_IDP_session(self):
        assert False


class WhenNavigatingToAuthPathWithGatewayIDPCookieSet(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, client):
        client.set_cookie('localhost', cookie.get('name'), cookie.get('value'))
        self.response = req(url_for('main.authentication_request'),
                            client.get, follow_redirects=True)

    def it_redirects_to_department_confirmation_with_department_set(
            self, client):

        assert department in self.response.soup.select_one("form legend").text

    def it_does_not_show_email_box(self):

        assert self.response.soup.select_one(".email-given") is None
