import pytest


class TestOIDCClient(object):

    @pytest.mark.xfail
    def test_send_authentication_request(self):
        assert False

    @pytest.mark.xfail
    def test_send_token_request(self):
        assert False

    @pytest.mark.xfail
    def test_send_userinfo_request(self):
        assert False

    @pytest.mark.xfail
    def test_send_logout_request(self):
        assert False
