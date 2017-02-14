import time
from urllib.parse import quote_plus as q_plus, urlparse

from flask import url_for
import pytest


@pytest.mark.usefixtures('live_server')
class When_on_to_idp_interstitial(object):

    @pytest.fixture(autouse=True)
    def setup_page(
            self, browser, email_address, submit_known_email_address):
        submit_known_email_address(email_address)
        browser.find_by_css('form button').click()

    def it_goes_to_the_idp_after_clicking_continue(
            self, browser, client_id, proxy, redirect_uri):

        browser.find_by_css('.pagination .next a').click()

        query = urlparse(browser.url).query

        assert browser.url.startswith(proxy)
        assert 'redirect_uri={}'.format(q_plus(redirect_uri)) in query
        assert 'client_id={}'.format(client_id) in query

    def it_goes_to_the_idp_after_waiting_for_countdown(
            self, browser, app, client_id, proxy, redirect_uri):
        counter = 0
        starting_url = url_for('main.to_idp', _external=True)
        meta_refresh_delay = app.config['META_REFRESH_DELAY']

        while browser.url == starting_url and counter <= meta_refresh_delay:
            time.sleep(1)
            counter += 1

        query = urlparse(browser.url).query

        assert browser.url.startswith(proxy)
        assert 'redirect_uri={}'.format(q_plus(redirect_uri)) in query
        assert 'client_id={}'.format(client_id) in query
