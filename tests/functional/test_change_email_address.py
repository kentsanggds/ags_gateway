from flask import url_for
import pytest


@pytest.mark.usefixtures('live_server')
class When_on_change_email_address_page(object):

    @pytest.fixture(autouse=True)
    def setup_page(
            self,
            email_address,
            submit_known_email_address,
            click_change_email):
        submit_known_email_address(email_address)
        click_change_email()

    def it_shows_the_email_address_supplied_in_the_textbox(
            self, browser, email_address):
        assert browser.find_by_css('#email_address').value == email_address

    def it_goes_to_dept_confirm_when_continue_clicked(self, browser):
        new_email = 'some.one@cabinetoffice.gov.uk'
        department = 'Cabinet Office'

        browser.fill('email_address', new_email)
        browser.find_by_css('form button').click()

        assert browser.url == url_for('main.confirm_dept', _external=True)
        assert browser.find_by_css('#confirm-dept>div>div').value == new_email
        assert department in browser.find_by_css('#confirm-dept > h2').value
