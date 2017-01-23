from flask import url_for
from tests.functional.user_flows import on_email_confirm_fill_in_then_continue
from tests.functional.user_flows import on_dept_confirm_click_change_email
from tests.functional.user_flows import yes_selected

email_address = 'some.one@digital.cabinet-office.gov.uk'


class When_on_change_email_address_page(object):

    def it_shows_the_email_address_supplied_in_the_textbox(
            self, live_server, browser):

        on_email_confirm_fill_in_then_continue(
            browser, yes_selected, email_address)

        on_dept_confirm_click_change_email(browser)

        assert browser.find_by_css('#email_address').value == email_address

    def it_goes_to_dept_confirm_when_continue_clicked(
            self, live_server, browser):

        on_email_confirm_fill_in_then_continue(
            browser, yes_selected, email_address)

        on_dept_confirm_click_change_email(browser)

        new_email = 'some.one@cabinetoffice.gov.uk'
        department = 'Cabinet Office'

        browser.fill('email_address', new_email)

        browser.find_by_css('form button').click()

        assert browser.url == url_for('main.confirm_dept', _external=True)
        assert browser.find_by_css('#confirm-dept>div>div').value == new_email
        assert department in browser.find_by_css('#confirm-dept > h2').value
