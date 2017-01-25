import pytest
from flask import url_for


@pytest.mark.usefixtures('live_server')
class When_on_confirm_email_with_yes_selected_and_valid_email(object):

    @pytest.fixture(autouse=True)
    def setup_page(
            self, browser, email_address, set_email_known, set_email_address):
        browser.visit(url_for('main.request_email_address', _external=True))
        set_email_known(True)
        set_email_address(email_address)

    def it_goes_to_department_confirm_when_continue_clicked(
            self, browser, email_address, department):

        browser.find_by_css('form button').click()

        assert browser.url == url_for('main.confirm_dept', _external=True)
        assert browser.find_by_css(
            '#confirm-dept>div>div').value == email_address
        assert department in browser.find_by_css('#confirm-dept > h2').value


@pytest.mark.usefixtures('live_server')
class When_on_confirm_email_with_no_selected(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, browser, email_address, set_email_known):
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
        assert not browser.find_by_name('email_address').visible

    def it_does_not_select_any_radio_buttons(self, browser):
        assert not browser.find_by_css('#email_known-0').checked
        assert not browser.find_by_css('#email_known-1').checked

    def it_stays_on_email_confirm_when_continue_clicked(self, browser):
        browser.find_by_css('form button').click()
        assert browser.url == url_for(
            'main.request_email_address', _external=True)
