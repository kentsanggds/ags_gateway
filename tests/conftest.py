import pytest

from responses import RequestsMock

from app.factory import create_app

from tests.oidc_testbed import MockOIDCProvider


@pytest.fixture
def config(issuer):
    return {'issuer': issuer}


@pytest.fixture
def issuer():
    return 'http://example.com'


@pytest.yield_fixture
def responses():
    with RequestsMock(assert_all_requests_are_fired=False) as patch:
        yield patch


@pytest.yield_fixture
def provider(responses, config):
    op = MockOIDCProvider(responses, config)
    op.init_endpoints()
    yield op
    op.remove_endpoints()


@pytest.yield_fixture
def app(provider, issuer):

    app = create_app(**{
        'TESTING': True,
        'PREFERRED_URL_SCHEME': 'http',
        'WTF_CSRF_ENABLED': False,
        'OIDC_CLIENT': {
            'issuer': issuer,
            'client_id': 'test-client',
            'client_secret': 'test-secret'
        },
        'OIDC_PROVIDER': {
            'issuer': 'https://localhost:5000',
            'subject_id_hash_salt': 'salt'
        },
        'META_REFRESH_DELAY': 1,
    })

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()
