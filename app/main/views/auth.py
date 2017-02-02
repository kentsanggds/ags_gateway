# -*- coding: utf-8 -*-
"""
Handle OIDC authentication requests
"""
import re

from flask import (
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from app.main import main
from app.main.forms import (
    ChangeEmailForm,
    DeptConfirmForm,
    DeptSelectForm,
    EmailForm,
    IdpConfirmForm,
    IdpSelectForm)


IDP_OF_LAST_RESORT = 'idp of last resort'

idp_names = {
    'gds-google': 'Government Digital Service',
    'co-digital': 'Cabinet Office',
    'ccs': 'Crown Commercial Service',
    'ad-saml': 'Azure AD SAML2',
}

idp_profiles = [
    {
        'id': 'gds-google',
        'idp_name': 'gds-google',
        'name': 'Government Digital Service',
        'email_pattern': '^[^@]+@digital\.cabinet-office\.gov\.uk$',
        'hint': 'All @digital.cabinet-office.gov.uk accounts'
    },
    {
        'id': 'co-digital',
        'idp_name': 'co-digital',
        'name': 'Cabinet Office',
        'email_pattern': '^[^@]+@cabinetoffice\.gov\.uk$',
        'hint': (
            'CO staff on the Official platform. @cabinet-office.gov.uk '
            'accounts only.')
    },
    {
        'id': 'ccs',
        'idp_name': 'co-digital',
        'name': 'Crown Commercial Service',
        'email_pattern': '^[^@]+@crowncommercial\.gov\.uk$',
        'hint': 'CCS staff, @crowncommercial.gov.uk accounts'
    },
    # csc.gov.uk
    # csep.gov.uk
    # cslearning.gov.uk
    # dexeu.gov.uk
    # ipa.gov.uk
    # odandd.gov.uk
    # orcl.gov.uk
    # pco.gov.uk
    {
        'id': 'ad-saml',
        'idp_name': 'ad-saml',
        'name': 'Civil Service Digital',
        'email_pattern': '^[^@]+@sso\.civilservice\.digital$',
        'hint': 'GDS staff in AGS, @sso.civilservice.digital accounts'
    },
]


def redirect_to_broker(idp):
    session['idp_hint'] = idp
    return redirect(url_for('broker.auth', idp_hint=idp))


def idp_from_email_address(email_address):
    return [idp for idp in idp_profiles if match_idp_email(idp, email_address)]


def match_idp_email(idp, email_address):
    return re.match(idp['email_pattern'], email_address)


def dept_from_idp_name(idp_name):
    idp = [idp['name'] for idp in idp_profiles if idp_name == idp['idp_name']]
    if idp:
        return ' or '.join(idp)
    return None


def idp_for_dept(dept):
    idp = session['auth_req'].get('dept_idp', '')
    if ',' in idp:
        idp = idp.split(',')
    return idp


def redirect_based_on_email_address(email_address):
    session['email_address'] = email_address
    idp = idp_from_email_address(email_address)

    if not idp:
        return redirect_to_broker(IDP_OF_LAST_RESORT)

    if len(idp) > 1:
        session['idp_choices'] = [item['id'] for item in idp]
        return redirect(url_for('.select_idp'))

    session['suggested_idp'] = idp[0]['idp_name']
    session['department_name'] = idp[0]['name']

    return redirect(url_for('.confirm_dept'))


@main.route('/auth', methods=['GET', 'POST'])
def authentication_request():
    if 'idp_choices' in session:
        del session['idp_choices']
    if 'suggested_idp' in session:
        del session['suggested_idp']
    if 'email_address' in session:
        del session['email_address']
    if 'department_name' in session:
        del session['department_name']

    session['auth_req'] = request.args

    if 'specific_idp' in request.args:
        return redirect_to_broker(request.args['specific_idp'])

    elif 'suggested_idp' in request.args:
        session['suggested_idp'] = request.args['suggested_idp']
        return redirect(url_for('.confirm_idp'))

    elif request.cookies.get('gateway_idp'):
        session['suggested_idp'] = request.cookies.get('gateway_idp')
        department = dept_from_idp_name(session['suggested_idp'])
        session['department_name'] = department
        return redirect(url_for('.confirm_dept'))

    return redirect(url_for('.request_email_address'))


@main.route('/change-email-address', methods=['GET', 'POST'])
def change_email_address():

    form = ChangeEmailForm()

    if form.validate_on_submit():
        return redirect_based_on_email_address(form.email_address.data)

    return render_template('views/auth/change_email.html', form=form)


@main.route('/confirm-email-address', methods=['GET', 'POST'])
def request_email_address():

    form = EmailForm()

    if form.validate_on_submit():

        if form.email_known.data == 'yes':
            return redirect_based_on_email_address(form.email_address.data)

        return redirect(url_for('.select_dept'))

    return render_template('views/auth/confirm_email.html', form=form)


@main.route('/select-identity-provider', methods=['GET', 'POST'])
def select_idp():

    def idp_choice(idp_id):
        return (idp_id, idp_names[idp_id])

    form = IdpSelectForm()
    form.idp.choices = map(idp_choice, session['idp_choices'])

    if form.validate_on_submit():
        return redirect_to_broker(form.idp.data)

    return render_template('views/auth/select_idp.html', form=form)


@main.route('/confirm-identity-provider', methods=['GET', 'POST'])
def confirm_idp():
    form = IdpConfirmForm()
    idp = session['suggested_idp']

    if form.validate_on_submit():

        if form.confirm.data == 'yes':
            return redirect_to_broker(idp)

        return redirect(url_for('.request_email_address'))

    return render_template('views/auth/confirm_idp.html', form=form)


@main.route('/select-department', methods=['GET', 'POST'])
def select_dept():

    form = DeptSelectForm()
    form.dept.choices = [(d['idp_name'], "{}|{}".format(d['name'], d['hint']))
                         for d in idp_profiles]

    if form.validate_on_submit():

        if form.dept.data:
            session['suggested_idp'] = form.dept.data
            return redirect(url_for('.to_idp'))

        return redirect_to_broker(IDP_OF_LAST_RESORT)

    return render_template('views/auth/select_dept.html', form=form)


@main.route('/search-dept')
def search_dept():
    # search_term = request.args.get('search_term', 0, type=str)
    return jsonify([
        {'id': 'GDS', 'descr': 'Government Digital Services'},
        {'id': 'CO', 'descr': 'Cabinet Office'},
        {'id': 'CCS', 'descr': 'Crown Commercial Service'},
    ])


@main.route('/confirm-department', methods=['GET', 'POST'])
def confirm_dept():
    form = DeptConfirmForm()

    if form.validate_on_submit():
        if form.confirm.data == 'yes':
            return redirect(url_for('.to_idp'))

        return redirect(url_for('.request_email_address'))

    return render_template('views/auth/confirm_dept.html', form=form)


@main.route('/to-idp')
def to_idp():
    resp = make_response(render_template('views/auth/to_idp.html'))
    resp.set_cookie('gateway_idp', session['suggested_idp'])
    return resp


@main.route('/to-service')
def to_service():
    return render_template('views/auth/to_service.html')
