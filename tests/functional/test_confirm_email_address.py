import pytest
from flask import url_for


@pytest.fixture
def set_email_known(browser):
    def do_set_email_known(known=True):
        value = 'yes' if known else 'no'
        browser.choose('email_known', value)
    return do_set_email_known


@pytest.fixture
def submit_email_address(browser):
    def do_submit_email_address(email_address):
        browser.fill('email_address', email_address)
        browser.find_by_css('form button').click()
    return do_submit_email_address


@pytest.fixture
def submit_known_email_address(
        browser,
        set_email_known,
        submit_email_address):

    def do_submit_known_email_address(email_address):
        browser.visit(url_for('main.request_email_address', _external=True))
        set_email_known(True)
        submit_email_address(email_address)
    return do_submit_known_email_address


@pytest.mark.usefixtures('live_server')
class When_on_confirm_email_with_yes_selected_and_valid_email(object):

    def it_goes_to_department_confirm_when_continue_clicked(
            self, browser, submit_known_email_address):
        email_address = 'some.one@digital.cabinet-office.gov.uk'
        department = 'Government Digital Service'

        submit_known_email_address(email_address)

        assert browser.url == url_for('main.confirm_dept', _external=True)
        assert browser.find_by_css(
            '#confirm-dept>div>div').value == email_address
        assert department in browser.find_by_css('#confirm-dept > h2').value


@pytest.mark.usefixtures('live_server')
class When_on_confirm_email_with_no_selected(object):

    def it_goes_to_select_department_when_continue_clicked(
            self, browser, set_email_known):

        browser.visit(url_for('main.request_email_address', _external=True))

        set_email_known(False)

        browser.find_by_css('form button').click()
        assert browser.url == url_for('main.select_dept', _external=True)


@pytest.mark.usefixtures('live_server')
class When_first_visiting_confirm_email(object):

    def it_does_not_show_email_textbox(self, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        assert not browser.find_by_name('email_address').visible

    def it_does_not_select_any_radio_buttons(self, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        assert not browser.find_by_css('#email_known-0').checked
        assert not browser.find_by_css('#email_known-1').checked

    def it_stays_on_email_confirm_when_continue_clicked(
            self, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        browser.find_by_css('form button').click()
        assert browser.url == url_for(
            'main.request_email_address', _external=True)
