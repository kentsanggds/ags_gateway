import time

from flask import url_for
import pytest


@pytest.mark.usefixtures('live_server')
class When_on_to_idp_interstitial(object):

    @pytest.fixture(autouse=True)
    def setup_page(
            self, browser, config, email_address, submit_known_email_address):
        self.oidc_client_issuer = config.get('OIDC_CLIENT')['issuer']

        submit_known_email_address(email_address)
        browser.find_by_css('form button').click()

    def it_goes_to_the_idp_after_clicking_continue(
            self, browser, responses):
        browser.find_by_css('.pagination .next a').click()

        assert browser.url.startswith(self.oidc_client_issuer)

    def it_goes_to_the_idp_after_waiting_for_countdown(self, browser, config):
        counter = 0
        starting_url = url_for('main.to_idp', _external=True)
        meta_refresh_delay = config.get('META_REFRESH_DELAY')

        while browser.url == starting_url:
            time.sleep(1)
            counter += 1

            # to prevent an endless loop
            if counter > meta_refresh_delay:
                break

        assert browser.url.startswith(self.oidc_client_issuer)
