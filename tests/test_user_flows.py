import pytest


class TestUserFlows(object):

    @pytest.mark.xfail
    def test_confirm_email_address(self):
        assert False

    @pytest.mark.xfail
    def test_change_email_address(self):
        assert False

    @pytest.mark.xfail
    def test_select_idp(self):
        assert False

    @pytest.mark.xfail
    def test_confirm_idp(self):
        assert False

    @pytest.mark.xfail
    def test_select_dept(self):
        assert False

    @pytest.mark.xfail
    def test_confirm_dept(self):
        assert False

    @pytest.mark.xfail
    def test_interstitial_to_idp(self):
        assert False

    @pytest.mark.xfail
    def test_interstitial_to_service(self):
        assert False
