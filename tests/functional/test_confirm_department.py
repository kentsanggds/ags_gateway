from flask import url_for


class When_first_visiting_confirm_department(object):

    def it_has_yes_selected(self, live_server, browser):
        browser.visit(url_for('main.confirm_dept', _external=True))

        assert browser.find_by_css('#confirm-0').checked

    def it_goes_to_idp_interstitial_when_continue_clicked(
            self, live_server, browser):
        browser.visit(url_for('main.confirm_dept', _external=True))

        browser.find_by_css('form button').click()

        assert browser.url == url_for('main.to_idp', _external=True)


class When_on_confirm_department_clicking_no(object):

    def it_goes_to_confirm_email_when_continue_clicked(
            self, live_server, browser):
        browser.visit(url_for('main.confirm_dept', _external=True))

        browser.choose('confirm', 'no')
        browser.find_by_css('form button').click()

        assert browser.url == url_for(
            'main.request_email_address', _external=True)
