import pytest

from responses import RequestsMock

from app.factory import create_app


@pytest.yield_fixture
def responses():
    with RequestsMock(assert_all_requests_are_fired=False) as patch:
        yield patch


@pytest.yield_fixture
def app():
    app = create_app(**{
        'TESTING': True,
        'PREFERRED_URL_SCHEME': 'http',
        'WTF_CSRF_ENABLED': False,
        'META_REFRESH_DELAY': 1,
    })

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()
