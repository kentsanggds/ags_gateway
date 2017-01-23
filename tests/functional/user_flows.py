from flask import url_for

no_selected = 'no'
yes_selected = 'yes'


def on_email_confirm_fill_in_then_continue(
        browser, email_known=None, email_address=None):
    browser.visit(url_for('main.request_email_address', _external=True))

    if email_known is not None:
        browser.choose('email_known', email_known)

    if email_address is not None:
        browser.fill('email_address', email_address)

    browser.find_by_css('form button').click()


def on_dept_confirm_click_change_email(browser):
    browser.find_by_css('#confirm-dept a').click()
