import pytest

from flask import url_for

from tests.conftest import responses, config  # noqa: F401
from tests.oidc_testbed import MockOIDCProvider
from tests.functional.mock_server import get_free_port, start_mock_server


@pytest.fixture
def email_address():
    return 'some.one@digital.cabinet-office.gov.uk'


@pytest.fixture
def department():
    return 'Government Digital Service'


@pytest.fixture
def mock_oidc_issuer():
    mock_server_port = get_free_port()
    start_mock_server(mock_server_port)
    return 'http://localhost:{port}/broker'.format(port=mock_server_port)


@pytest.yield_fixture   # noqa: F811
def provider(responses, mock_oidc_issuer):
    global config
    config['issuer'] = mock_oidc_issuer

    op = MockOIDCProvider(responses, config)
    op.init_endpoints()
    yield op
    op.remove_endpoints()


@pytest.fixture
def set_email_known(browser):
    def do_set_email_known(known=True):
        value = 'yes' if known else 'no'
        browser.choose('email_known', value)
    return do_set_email_known


@pytest.fixture
def set_email_address(browser):
    def do_set_email_address(email_address):
        browser.fill('email_address', email_address)
    return do_set_email_address


@pytest.fixture
def submit_known_email_address(
        browser, set_email_known, set_email_address):
    def do_submit_known_email_address(email_address):
        browser.visit(url_for('main.request_email_address', _external=True))
        set_email_known(True)
        set_email_address(email_address)
        browser.find_by_css('form button').click()
    return do_submit_known_email_address
