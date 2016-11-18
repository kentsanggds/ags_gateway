from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Optional


yesno = [(True, 'Yes'), (False, 'No')]


def coerce_bool(x):
    if x == 'False':
        return False
    return bool(x)


class EmailForm(FlaskForm):
    email_known = RadioField(choices=yesno, coerce=coerce_bool)
    email_address = EmailField('Email address', validators=[
        Optional(), Email()])


class IdpConfirmForm(FlaskForm):
    confirm = RadioField(choices=yesno, coerce=coerce_bool)


class IdpSelectForm(FlaskForm):
    idp = RadioField(choices=[])


class DeptSelectForm(FlaskForm):
    dept = RadioField(choices=[])
