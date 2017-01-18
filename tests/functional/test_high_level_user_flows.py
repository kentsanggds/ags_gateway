import pytest
from flask import url_for


email_depts = [
    ('some.one@digital.cabinet-office.gov.uk', 'Government Digital Service')]


class TestUserFlowsFromEmailConfirmation(object):

    @pytest.mark.parametrize("email_address,department", email_depts)
    def test_select_yes_then_enters_email_then_click_to_department_confirm(
            self, live_server, browser, email_address, department):

        browser.visit(url_for('main.request_email_address', _external=True))

        browser.choose('email_known', 'yes')
        browser.fill('email_address', email_address)

        browser.find_by_css('form button').click()

        assert browser.find_by_css(
            '#confirm-dept > div > div').value == email_address
        assert department in browser.find_by_css(
            '#confirm-dept > h2').value
