import mock
import pytest

from app.factory import create_app


def _provider_config(*args, **kwargs):
    pass


@pytest.fixture(scope='session')
def app_(request):
    with mock.patch('oic.oic.Client.provider_config', _provider_config):
        app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app
