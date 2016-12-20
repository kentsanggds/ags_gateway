from flask import session, url_for
import pytest

from app.main.views.auth import idp_profiles


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

    def test_change_email_address(self, app_):
        url = url_for('main.change_email_address')
        data = {
            'email_address': 'test@digital.cabinet-office.gov.uk'
        }
        with app_.test_client() as c:
            assert c.get(url).status_code == 200
            resp = c.post(url, data=data)
            assert resp.status_code == 302
            assert resp.location.endswith(url_for('main.confirm_dept'))
            assert session['email_address'] == data['email_address']
            assert session['suggested_idp'] == 'gds-google'
            assert session['department_name'] == 'Government Digital Service'

    @pytest.mark.parametrize("idp_id", [
        'gds-google',
        'co-digital',
        'ad-saml',
    ])
    def test_select_idp(self, app_, idp_id):
        url = url_for('main.select_idp')
        data = {
            'idp': idp_id
        }
        with app_.test_client() as c:
            with c.session_transaction() as sess:
                sess['idp_choices'] = [item['id'] for item in idp_profiles]
            assert c.get(url).status_code == 200
            resp = c.post(url, data=data)
            assert resp.status_code == 302
            assert resp.location.endswith('/broker?idp_hint=%s' % idp_id)

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
