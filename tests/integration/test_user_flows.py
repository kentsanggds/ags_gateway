from bs4 import BeautifulSoup
from flask import session, url_for
import pytest

from app.main.views.auth import idp_profiles


email_idp_name = [
    ('test@digital.cabinet-office.gov.uk', 'gds-google',
     'Government Digital Service'),
    ('test.test@cabinetoffice.gov.uk', 'co-digital', 'Cabinet Office'),
    ('test@sso.civilservice.digital', 'ad-saml', 'Civil Service Digital'),
]


class TestUserFlows(object):

    def assert_meta_refresh(self, response, seconds_delay, url):
        content = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        meta = content.find(
            'meta',
            attrs={
                'http-equiv': 'refresh',
                'content': '{seconds_delay}; url={url}'.format(
                    seconds_delay=seconds_delay, url=url)})
        assert meta is not None

    @pytest.mark.parametrize("email, idp, name", email_idp_name)
    def test_confirm_email_address(self, client, email, idp, name):
        url = url_for('main.request_email_address')
        data = {
            'email_known': 'yes',
            'email_address': email
        }

        assert client.get(url).status_code == 200

        resp = client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location.endswith(url_for('main.confirm_dept'))

    @pytest.mark.xfail
    @pytest.mark.parametrize("email", [
        'test@digital.cabinetoffice.gov.uk',
        'test.test@cabinet-office.gov.uk',
        'test@sso.civilservice.uk',
        'test@test.com',
    ])
    def test_confirm_email_address_broker_lookup_redirect(self, client, email):
        data = {
            'email_known': 'yes',
            'email_address': email
        }

        resp = client.post(url_for('main.request_email_address'), data=data)
        assert resp.status_code == 302
        assert resp.location.endswith(
            url_for('broker.auth', idp_hint=session['idp_hint']))

    @pytest.mark.parametrize("email, idp, name", email_idp_name)
    def test_change_email_address(self, client, email, idp, name):
        url = url_for('main.change_email_address')
        data = {
            'email_address': email
        }

        assert client.get(url).status_code == 200

        resp = client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location.endswith(url_for('main.confirm_dept'))

    @pytest.mark.parametrize("idp_id", [
        'gds-google',
        'co-digital',
        'ad-saml',
    ])
    def test_select_idp(self, client, idp_id):
        url = url_for('main.select_idp')
        data = {
            'idp': idp_id
        }

        with client.session_transaction() as sess:
            sess['idp_choices'] = [item['id'] for item in idp_profiles]

        assert client.get(url).status_code == 200

        resp = client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location.endswith(
            url_for('broker.auth', idp_hint=idp_id))

    @pytest.mark.parametrize("idp_id, choice, endpoint, values", [
        ('gds-google', 'yes', 'broker.auth', {'idp_hint': 'gds-google'}),
        ('co-digital', 'yes', 'broker.auth', {'idp_hint': 'co-digital'}),
        ('ad-saml', 'yes', 'broker.auth', {'idp_hint': 'ad-saml'}),
        ('gds-google', 'no', 'main.request_email_address', {}),
        ('co-digital', 'no', 'main.request_email_address', {}),
        ('ad-saml', 'no', 'main.request_email_address', {}),
    ])
    def test_confirm_idp(self, client, idp_id, choice, endpoint, values):
        url = url_for('main.confirm_idp')
        data = {
            'confirm': choice
        }

        with client.session_transaction() as sess:
            sess['suggested_idp'] = idp_id

        assert client.get(url).status_code == 200

        resp = client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location.endswith(url_for(endpoint, **values))

    @pytest.mark.parametrize("idp_id", [
        'gds-google',
        'co-digital',
        'ad-saml',
    ])
    def test_select_dept(self, client, idp_id):
        url = url_for('main.select_dept')
        data = {
            'dept': idp_id
        }

        assert client.get(url).status_code == 200

        resp = client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location.endswith(url_for('main.to_idp'))

    @pytest.mark.parametrize("email, idp, name", email_idp_name)
    def test_confirm_dept(self, client, email, idp, name):
        url = url_for('main.confirm_dept')
        data = {
            'confirm': 'yes'
        }

        with client.session_transaction() as sess:
            sess['suggested_idp'] = idp
            sess["department_name"] = name
            sess["email_address"] = email

        resp = client.get(url)
        assert resp.status_code == 200
        content = str(resp.data)
        assert email in content
        assert name in content

        resp = client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location.endswith(url_for('main.to_idp'))

    @pytest.mark.xfail
    @pytest.mark.parametrize("idp_id", [
        'gds-google',
        'co-digital',
        'ad-saml',
    ])
    def test_interstitial_to_idp(self, app_, client, idp_id):
        url = url_for('main.to_idp')

        with client.session_transaction() as sess:
            sess['suggested_idp'] = idp_id

        resp = client.get(url)
        assert resp.status_code == 200
        self.assert_meta_refresh(resp, app_.config['META_REFRESH_DELAY'],
                                 url_for('broker.auth', idp_hint=idp_id))

    @pytest.mark.xfail
    def test_interstitial_to_service(self, app_, client):
        url = url_for('main.to_service')

        with client.session_transaction() as sess:
            sess['auth_redirect'] = '/url'

        resp = client.get(url)
        assert resp.status_code == 200
        self.assert_meta_refresh(resp, app_.config['META_REFRESH_DELAY'],
                                 session['auth_redirect'])
