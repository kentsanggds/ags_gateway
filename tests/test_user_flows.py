from flask import session, url_for
import pytest


class TestUserFlows(object):

    @pytest.mark.parametrize("email, idp, name", [
        ('test@digital.cabinet-office.gov.uk', 'gds-google',
         'Government Digital Service'),
        ('test.test@cabinetoffice.gov.uk', 'co-digital', 'Cabinet Office'),
        ('test@sso.civilservice.uk', 'ad-saml', 'Civil Service Digital'),
    ])
    def test_confirm_email_address(self, app_, email, idp, name):
        url = url_for('main.request_email_address')
        data = {
            'email_known': 'yes',
            'email_address': email
        }
        with app_.test_client() as c:
            assert c.get(url).status_code == 200
            resp = c.post(url, data=data)
            assert resp.status_code == 302
            assert resp.location.endswith(url_for('main.confirm_dept'))
            assert session['email_address'] == email
            assert session['suggested_idp'] == idp
            assert session['department_name'] == name

    @pytest.mark.parametrize("email", [
        'test@digital.cabinetoffice.gov.uk',
        'test.test@cabinet-office.gov.uk',
        'test@sso.civilservice.digital',
        'test@test.com',
    ])
    def test_confirm_email_address_broker_lookup_redirect(self, app_, email):
        url = url_for('main.request_email_address')
        data = {
            'email_known': 'yes',
            'email_address': email
        }
        with app_.test_client() as c:
            resp = c.post(url, data=data)
            assert session['idp_hint'] == 'idp of last resort'
            assert resp.status_code == 302
            assert resp.location.endswith(
                url_for('broker.auth', idp_hint=session['idp_hint']))
    @pytest.mark.xfail
    def test_change_email_address(self):
        assert False

    @pytest.mark.xfail
    def test_select_idp(self):
        assert False

    @pytest.mark.xfail
    def test_confirm_idp(self):
        assert False

    @pytest.mark.xfail
    def test_select_dept(self):
        assert False

    @pytest.mark.xfail
    def test_confirm_dept(self):
        assert False

    @pytest.mark.xfail
    def test_interstitial_to_idp(self):
        assert False

    @pytest.mark.xfail
    def test_interstitial_to_service(self):
        assert False
