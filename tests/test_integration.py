from flask import url_for


class TestIntegration(object):

    def test_get_ags_gateway(self, live_server, browser):
        browser.visit(url_for('main.request_email_address', _external=True))

        assert ('GOV.UK - The best place to find government services and '
                'information') in browser.title
