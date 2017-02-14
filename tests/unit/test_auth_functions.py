from mock import patch

from app.main.views.auth import dept_from_idp_name, idp_from_email_address

idp_name = 'gds-google'
department = 'Government Digital Service'
idp_name_alt = 'co-digital'

idp_profiles = [
    {
        'idp_name': 'gds-google',
        'name': 'Government Digital Service',
    },
    {
        'idp_name': 'co-digital',
        'name': 'Cabinet Office',
    },
    {
        'idp_name': 'co-digital',
        'name': 'Crown Commercial Service',
    },
]


class WhenTestingDeptFromIDPName(object):

    @patch('app.main.views.auth.idp_profiles', idp_profiles)
    def it_returns_idp_with_valid_idp_name(self):
        assert dept_from_idp_name(idp_name) == department

    def it_returns_None_with_unknown_idp_name(self):
        assert dept_from_idp_name('unknown') is None

    @patch('app.main.views.auth.idp_profiles', idp_profiles)
    def it_returns_OR_seperated_list_for_multiple_departments(self):
        assert ' or ' in dept_from_idp_name(idp_name_alt)


class WhenTestingIDPFromEmailAddress(object):

    def it_returns_HOD_IDP_for_Home_Office_Digital_email_address(self):
        email_address = 'some.one@digital.homeoffice.gov.uk'
        idp = idp_from_email_address(email_address)

        assert idp[0]['idp_name'] == 'HOD'
