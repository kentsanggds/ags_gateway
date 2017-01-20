import pytest
from flask import url_for

email_depts = [('some.one@digital.cabinet-office.gov.uk',
                'Government Digital Service')]


class When_on_confirm_email_with_yes_selected_and_valid_email(object):

    @pytest.mark.parametrize("email_address,department", email_depts)
    def it_goes_to_department_confirm_when_continue_clicked(
            self, live_server, browser, email_address, department):
        browser.visit(url_for('main.request_email_address', _external=True))

        browser.choose('email_known', 'yes')
        browser.fill('email_address', email_address)

        browser.find_by_css('form button').click()

        assert browser.url == url_for('main.confirm_dept', _external=True)
        assert browser.find_by_css(
            '#confirm-dept > div > div').value == email_address
        assert department in browser.find_by_css(
            '#confirm-dept > h2').value


class When_on_confirm_email_with_no_selected(object):

    def it_goes_to_select_department_when_continue_clicked(
            self, live_server, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        browser.choose('email_known', 'no')
        browser.find_by_css('form button').click()

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

        browser.visit(url_for('main.request_email_address', _external=True))
        browser.find_by_css('form button').click()

        assert browser.url == url_for(
            'main.request_email_address', _external=True)


class When_first_visiting_confirm_department(object):
    
    def it_has_yes_selected(self, live_server, browser):
        browser.visit(url_for('main.confirm_dept', _external=True))

        assert browser.find_by_css('#confirm-0').checked

    @pytest.mark.xfail
    def it_has_correct_department_for_email(self, live_server, browser):

        assert False

    @pytest.mark.xfail
    def it_goes_to_idp_interstitial_when_continue_clicked(
            self, live_server, browser):

        assert False

    @pytest.mark.xfail
    def it_goes_to_change_email_with_correct_email_filled_in(
            self, live_server, browser):
        assert False
