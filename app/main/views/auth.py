# -*- coding: utf-8 -*-
"""
Handle OIDC authentication requests
"""

from flask import redirect, render_template, request, session, url_for

from app.main import main
from app.main.forms import (
    DeptSelectForm,
    EmailForm,
    IdpConfirmForm,
    IdpSelectForm)
from app.oidc import AuthenticationRequest, AuthenticationRequestError


IDP_OF_LAST_RESORT = 'idp of last resort'

idp_names = {
    'google': 'Government Digital Service',
    'dex': 'Cabinet Office',
    'keycloak': 'Ministry of Justice',
}


def redirect_to_broker(idp):
    return 'redirect_to_broker({})'.format(idp)


def idp_from_email_address(email_address):
    idp = session['auth_req'].get('email_idp', '')
    if ',' in idp:
        idp = idp.split(',')
    return idp


def idp_for_dept(dept):
    idp = session['auth_req'].get('dept_idp', '')
    if ',' in idp:
        idp = idp.split(',')
    return idp


@main.route('/auth', methods=['GET', 'POST'])
def authentication_request():
    if 'idp_choices' in session:
        del session['idp_choices']
    if 'suggested_idp' in session:
        del session['suggested_idp']
    if 'email_address' in session:
        del session['email_address']

    try:
        auth_req = AuthenticationRequest(request)

    except AuthenticationRequestError as err:
        return err

    # TODO - OIDC spec 3.1.2.2 item 4

    # session['auth_req'] = auth_req
    session['auth_req'] = request.args

    if auth_req.specific_idp:
        return redirect_to_broker(auth_req.specific_idp)

    elif auth_req.suggested_idp:
        session['suggested_idp'] = auth_req.suggested_idp
        return redirect(url_for('.confirm_idp'))

    return redirect(url_for('.request_email_address'))


@main.route('/confirm-email-address', methods=['GET', 'POST'])
def request_email_address():

    form = EmailForm()

    if form.validate_on_submit():

        if form.email_known.data:

            session['email_address'] = form.email_address.data
            idp = idp_from_email_address(form.email_address.data)

            if idp is None:
                return redirect_to_broker(IDP_OF_LAST_RESORT)

            if isinstance(idp, list):
                session['idp_choices'] = idp
                return redirect(url_for('.select_idp'))

            return redirect_to_broker(idp)

        else:
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

        if form.confirm.data:
            return redirect_to_broker(idp)

        return redirect(url_for('.request_email_address'))

    return render_template('views/auth/confirm_idp.html', form=form)


@main.route('/select-department', methods=['GET', 'POST'])
def select_dept():

    form = DeptSelectForm()

    if form.validate_on_submit():

        if form.dept.data:
            session['suggested_idp'] = idp_for_dept(form.dept.data)
            return redirect(url_for('.confirm_idp'))

        return redirect_to_broker(IDP_OF_LAST_RESORT)

    return render_template('views/auth/select_dept.html', form=form)
