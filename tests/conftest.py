import mock
import pytest

from app.factory import create_app


@pytest.fixture(scope='session')
def app(request):
    app = create_app(**{
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'OIDC_CLIENT': {
            'issuer': 'https://example.com',
            'client_id': 'test-client',
            'client_secret': 'test-secret'},
    })

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app
