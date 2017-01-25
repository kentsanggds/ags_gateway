import pytest
from flask import url_for


@pytest.mark.usefixtures('live_server')
class When_on_to_idp_interstitial(object):

    @pytest.fixture(autouse=True)
    def setup_page(
            self,
            browser,
            email_address,
            submit_known_email_address,
            click_continue_button):
        submit_known_email_address(email_address)
        click_continue_button()

    @pytest.mark.xfail
    def it_goes_to_the_idp_after_waiting_for_countdown(self, browser, config):
        assert False

    @pytest.mark.xfail
    def it_goes_to_the_idp_after_clicking_continue(self, browser):
        assert False
