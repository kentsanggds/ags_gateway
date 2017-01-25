import pytest

from flask import url_for


@pytest.fixture
def email_address():
    return 'some.one@digital.cabinet-office.gov.uk'


@pytest.fixture
def department():
    return 'Government Digital Service'


@pytest.fixture
def set_email_known(browser):
    def do_set_email_known(known=True):
        value = 'yes' if known else 'no'
        browser.choose('email_known', value)
    return do_set_email_known


@pytest.fixture
def set_email_address(browser):
    def do_set_email_address(email_address):
        browser.fill('email_address', email_address)
    return do_set_email_address


@pytest.fixture
def submit_known_email_address(
        browser, email_address, set_email_known, set_email_address):
    def do_submit_known_email_address(email_address):
        browser.visit(url_for('main.request_email_address', _external=True))
        set_email_known(True)
        set_email_address(email_address)
        browser.find_by_css('form button').click()
    return do_submit_known_email_address
