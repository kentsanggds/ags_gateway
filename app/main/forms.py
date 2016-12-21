from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Optional, Required

yesno = [('yes', 'Yes'), ('no', 'No')]


class DeptConfirmForm(FlaskForm):
    confirm = RadioField(choices=yesno, default='yes')


class DeptSelectForm(FlaskForm):
    dept = RadioField(choices=[])


class ChangeEmailForm(FlaskForm):
    email_address = EmailField('Email', validators=[
        Required(), Email()])


class EmailForm(FlaskForm):
    email_known = RadioField(choices=yesno, default='yes')
    email_address = EmailField('Email', validators=[
        Optional(), Email()])


class IdpConfirmForm(FlaskForm):
    confirm = RadioField(choices=yesno)


class IdpSelectForm(FlaskForm):
    idp = RadioField(choices=[])
