import pytest

from app.factory import create_app
from flask import url_for
from responses import RequestsMock
from tests.oidc_testbed import MockOIDCProvider


config = {
    'issuer': 'http://example.com',
}


@pytest.yield_fixture
def responses():
    with RequestsMock(assert_all_requests_are_fired=False) as patch:
        yield patch


@pytest.yield_fixture
def provider(responses):
    op = MockOIDCProvider(responses, config)
    op.init_endpoints()
    yield op
    op.remove_endpoints()


@pytest.yield_fixture
def app(provider):
    app = create_app(**{
        'TESTING': True,
        'PREFERRED_URL_SCHEME': 'http',
        'WTF_CSRF_ENABLED': False,
        'OIDC_CLIENT': {
            'issuer': config['issuer'],
            'client_id': 'test-client',
            'client_secret': 'test-secret'
        },
        'OIDC_PROVIDER': {
            'issuer': 'https://localhost:5000',
            'subject_id_hash_salt': 'salt'
        }
    })

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def set_email_known(browser):
    def do_set_email_known(known=True):
        value = 'yes' if known else 'no'
        browser.choose('email_known', value)
    return do_set_email_known


@pytest.fixture
def submit_email_address(browser):
    def do_submit_email_address(email_address):
        browser.fill('email_address', email_address)
        browser.find_by_css('form button').click()
    return do_submit_email_address


@pytest.fixture
def submit_known_email_address(
        browser,
        set_email_known,
        submit_email_address):

    def do_submit_known_email_address(email_address):
        browser.visit(url_for('main.request_email_address', _external=True))
        set_email_known(True)
        submit_email_address(email_address)
    return do_submit_known_email_address
