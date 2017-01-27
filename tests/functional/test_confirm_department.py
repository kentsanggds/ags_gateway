from flask import url_for
import pytest


@pytest.mark.usefixtures('live_server')
class When_first_visiting_confirm_department(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, email_address, submit_known_email_address):
        submit_known_email_address(email_address)

    def it_has_yes_selected(self, browser):
        assert browser.find_by_css('#confirm-0').checked

    def it_goes_to_idp_interstitial_when_continue_clicked(self, browser):
        browser.find_by_css('form button').click()

        assert browser.url == url_for('main.to_idp', _external=True)


@pytest.mark.usefixtures('live_server')
class When_on_confirm_department_clicking_no(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, browser, email_address, submit_known_email_address):
        submit_known_email_address(email_address)
        browser.choose('confirm', 'no')

    def it_goes_to_confirm_email_when_continue_clicked(self, browser):
        browser.find_by_css('form button').click()

        assert browser.url == url_for(
            'main.request_email_address', _external=True)
