from flask import url_for

from selenium.webdriver.common.keys import Keys


class TestFunctional(object):

    def test_can_show_email_confirmation(self, live_server, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        assert ('GOV.UK - The best place to find government services and '
                'information') in browser.title

        assert browser.is_text_present('Do you know your work email?')

    def test_can_go_from_email_confirm_to_department_confirmation(
            self, live_server, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        browser.choose('email_known', 'yes')

        browser.is_element_present_by_css(
            "#email_address", wait_time=0.1)

        browser.fill('email_address',
                     'some.one@digital.cabinet-office.gov.uk')

        browser.driver.find_element_by_xpath(
            '//*[@id="content"]/form/div[3]/button').send_keys(Keys.ENTER)
        assert browser.is_text_present(
            'Email address you provided')
        assert browser.is_text_present(
            'some.one@digital.cabinet-office.gov.uk')
