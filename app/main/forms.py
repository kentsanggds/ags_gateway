from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Optional, Required

yesno = [('yes', 'Yes'), ('no', 'No')]


def coerce_bool(x):
    if x == 'False':
        return False
    return bool(x)


class DeptConfirmForm(FlaskForm):
    confirm = RadioField(choices=yesno, default='Yes')


class DeptSelectForm(FlaskForm):
    dept = RadioField(choices=[])


class ChangeEmailForm(FlaskForm):
    email_address = EmailField('Email', validators=[
        Required(), Email()])


class EmailForm(FlaskForm):
    email_known = RadioField(choices=yesno, default='Yes')
    email_address = EmailField('Email', validators=[
        Optional(), Email()])


class IdpConfirmForm(FlaskForm):
    confirm = RadioField(choices=yesno, coerce=coerce_bool)


class IdpSelectForm(FlaskForm):
    idp = RadioField(choices=[])
