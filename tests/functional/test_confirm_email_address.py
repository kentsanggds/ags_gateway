import pytest
from flask import url_for


@pytest.mark.usefixtures('live_server')
class When_on_confirm_email_with_yes_selected(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, browser, set_email_known):
        browser.visit(url_for('main.request_email_address', _external=True))
        set_email_known(True)

    def it_goes_to_department_confirm_when_valid_email_submitted(
            self, browser, email_address, department, set_email_address):

        set_email_address(email_address)

        browser.find_by_css('form button').click()

        assert browser.url == url_for('main.confirm_dept', _external=True)
        assert browser.find_by_css(
            '#confirm-dept>div>div').value == email_address
        assert department in browser.find_by_css('#confirm-dept > h2').value

    def it_shows_an_error_if_no_email_address_submitted(self, browser):

        browser.find_by_css('form button').click()

        assert browser.url == url_for(
            'main.request_email_address', _external=True)
        assert browser.find_by_css('label[for=email_address] .error-message')


@pytest.mark.usefixtures('live_server')
class When_on_confirm_email_with_no_selected(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, browser, set_email_known):
        browser.visit(url_for('main.request_email_address', _external=True))
        set_email_known(False)

    def it_goes_to_select_department_when_continue_clicked(
            self, browser, set_email_known):

        browser.find_by_css('form button').click()
        assert browser.url == url_for('main.select_dept', _external=True)


@pytest.mark.usefixtures('live_server')
class When_first_visiting_confirm_email(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

    def it_does_not_show_email_textbox(self, browser):
        assert browser.find_by_name('email_address').visible is False

    def it_does_not_select_any_radio_buttons(self, browser):
        assert browser.find_by_css('#email_known-0').checked is False
        assert browser.find_by_css('#email_known-1').checked is False

    def it_stays_on_email_confirm_when_continue_clicked(self, browser):
        browser.find_by_css('form button').click()
        assert browser.url == url_for(
            'main.request_email_address', _external=True)
