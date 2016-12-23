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


@pytest.yield_fixture
def client(app_):
    with app_.test_client() as c:
        yield c


@pytest.yield_fixture
def request_params():
    return {
        'grant_type': 'authorization_code',
        'code': 'SplxlOBeZQQYbYS6WxSbIA',
        'redirect_uri': '/mock_url',
    }


@pytest.yield_fixture
def request_headers(app_):
    return {
        'Content-Length': '0',
        'Host': app_.config['SERVER_NAME'],
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW',
    }


@pytest.yield_fixture
def token_response():
    return {
        'access_token': 'SlAV32hkKG',
        'token_type': 'Bearer',
        'refresh_token': '8xLOxBtZp8',
        'expires_in': 3600,
        'id_token': '''eyJhbGciOiJSUzI1NiIsImtpZCI6IjFlOWdkazcifQ.ewogImlzc
    yI6ICJodHRwOi8vc2VydmVyLmV4YW1wbGUuY29tIiwKICJzdWIiOiAiMjQ4Mjg5
    NzYxMDAxIiwKICJhdWQiOiAiczZCaGRSa3F0MyIsCiAibm9uY2UiOiAibi0wUzZ
    fV3pBMk1qIiwKICJleHAiOiAxMzExMjgxOTcwLAogImlhdCI6IDEzMTEyODA5Nz
    AKfQ.ggW8hZ1EuVLuxNuuIJKX_V8a_OMXzR0EHR9R6jgdqrOOF4daGU96Sr_P6q
    Jp6IcmD3HP99Obi1PRs-cwh3LO-p146waJ8IhehcwL7F09JdijmBqkvPeB2T9CJ
    NqeGpe-gccMg4vfKjkM8FcGvnzZUN4_KSP0aAp1tOJ1zZwgjxqGByKHiOtX7Tpd
    QyHE5lcMiKPXfEIQILVq0pc_E2DzL7emopWoaoZTF_m0_N0YzFC6g6EJbOEoRoS
    K5hoDalrcvRYLSrQAZZKflyuVCyixEoV9GfNQC3_osjzw2PAithfubEEBLuVVk4
    XUVrWOLrLl0nx7RkKU8NXNHq-rvKMzqg'''
    }
