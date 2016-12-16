import pytest


class TestOIDCProvider(object):

    @pytest.mark.xfail
    def test_handle_auth_request(self):
        assert False

    @pytest.mark.xfail
    def test_handle_token_request(self):
        assert False

    @pytest.mark.xfail
    def test_handle_userinfo_request(self):
        assert False

    @pytest.mark.xfail
    def test_userinfo_requested_claims(self):
        assert False

    @pytest.mark.xfail
    def test_handle_end_session_request(self):
        assert False
