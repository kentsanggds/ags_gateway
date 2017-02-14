import time

from flask import url_for
import pytest


@pytest.mark.usefixtures('live_server')
class When_on_to_idp_interstitial(object):

    @pytest.fixture(autouse=True)
    def setup_page(
            self, browser, app, email_address, submit_known_email_address):
        self.oidc_client_issuer = app.config['OIDC_CLIENT']['issuer']

        submit_known_email_address(email_address)
        browser.find_by_css('form button').click()

    def it_goes_to_the_idp_after_clicking_continue(
            self, browser, responses):
        browser.find_by_css('.pagination .next a').click()

        assert browser.url.startswith(self.oidc_client_issuer)

    def it_goes_to_the_idp_after_waiting_for_countdown(self, browser, app):
        counter = 0
        starting_url = url_for('main.to_idp', _external=True)
        meta_refresh_delay = app.config['META_REFRESH_DELAY']

        while browser.url == starting_url and counter <= meta_refresh_delay:
            time.sleep(1)
            counter += 1

        assert browser.url.startswith(self.oidc_client_issuer)
