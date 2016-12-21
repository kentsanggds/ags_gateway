import pytest
from werkzeug.datastructures import MultiDict

from app.main.forms import IdpConfirmForm


class TestUserFlowForms(object):

    @pytest.mark.parametrize("value, coerced", [
        ('yes', 'yes'),
        ('yes', 'yes'),
    ])
    def test_idp_confirm_form(self, value, coerced):
        form = IdpConfirmForm(formdata=MultiDict([('confirm', value)]))
        assert form.confirm.choices == [('yes', 'Yes'), ('no', 'No')]
        assert form.confirm.data == coerced
        form.validate()
        assert form.errors == {}
