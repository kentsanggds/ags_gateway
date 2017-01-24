from flask import url_for
from tests.functional.user_flows import on_email_confirm_fill_in_then_continue
from tests.functional.user_flows import yes_selected, no_selected


class When_on_confirm_email_with_yes_selected_and_valid_email(object):

    def it_goes_to_department_confirm_when_continue_clicked(
            self, live_server, browser):

        email_address = 'some.one@digital.cabinet-office.gov.uk'
        department = 'Government Digital Service'

        on_email_confirm_fill_in_then_continue(
            browser, yes_selected, email_address)

        assert browser.url == url_for('main.confirm_dept', _external=True)
        assert browser.find_by_css(
            '#confirm-dept>div>div').value == email_address
        assert department in browser.find_by_css('#confirm-dept > h2').value


class When_on_confirm_email_with_no_selected(object):

    def it_goes_to_select_department_when_continue_clicked(
            self, live_server, browser):

        on_email_confirm_fill_in_then_continue(browser, no_selected)

        assert browser.url == url_for('main.select_dept', _external=True)


class When_first_visiting_confirm_email(object):

    def it_does_not_show_email_textbox(self, live_server, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        assert not browser.find_by_name('email_address').visible

    def it_does_not_select_any_radio_buttons(self, live_server, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        assert not browser.find_by_css('#email_known-0').checked
        assert not browser.find_by_css('#email_known-1').checked

    def it_does_not_go_to_department_confirm_when_continue_clicked(
            self, live_server, browser):

        on_email_confirm_fill_in_then_continue(browser)

        assert browser.url == url_for(
            'main.request_email_address', _external=True)
