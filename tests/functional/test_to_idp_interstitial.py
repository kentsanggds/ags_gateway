import time

from flask import url_for
import pytest


@pytest.mark.usefixtures('live_server')
class When_on_to_idp_interstitial(object):

    @pytest.fixture(autouse=True)
    def setup_page(
            self,
            email_address,
            submit_known_email_address,
            click_continue_button):
        submit_known_email_address(email_address)
        click_continue_button()

    def it_goes_to_the_idp_after_clicking_continue(
            self, browser, config, responses):

        browser.find_by_css(
            '#content>div.pagination>ul>'
            'li>a>span.pagination-text>span').click()

        assert browser.url.startswith(config.get('OIDC_CLIENT')['issuer'])

    def it_goes_to_the_idp_after_waiting_for_countdown(self, browser, config):
        counter = 0
        while browser.url == url_for('main.to_idp', _external=True):
            time.sleep(1)
            counter += 1

            # to prevent an endless loop
            if counter > config.get('META_REFRESH_DELAY'):
                break

        assert browser.url.startswith(config.get('OIDC_CLIENT')['issuer'])
