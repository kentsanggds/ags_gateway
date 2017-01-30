from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired, Optional, Required

YES = 'yes'
NO = 'no'
yesno = [(YES, 'Yes'), (NO, 'No')]


class DeptConfirmForm(FlaskForm):
    confirm = RadioField(choices=yesno, default=YES)


class DeptSelectForm(FlaskForm):
    dept = RadioField(choices=[])


class ChangeEmailForm(FlaskForm):
    email_address = EmailField('Email', validators=[
        Required(), Email()])


class RequiredIf(InputRequired):

    def __init__(self, field_name, value, *args, **kwargs):
        self.requiring_field_name = field_name
        self.requiring_value = value
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        requiring_field = form._fields.get(self.requiring_field_name)

        if requiring_field:

            if requiring_field.data == self.requiring_value:
                super(RequiredIf, self).__call__(form, field)

            else:
                return Optional()(form, field)


class EmailForm(FlaskForm):
    email_known = RadioField(choices=yesno)
    email_address = EmailField(
        'Email',
        validators=[
            RequiredIf(
                'email_known',
                value=YES,
                message='You must enter a valid email address'),
            Email(),
        ]
    )


class IdpConfirmForm(FlaskForm):
    confirm = RadioField(choices=yesno)


class IdpSelectForm(FlaskForm):
    idp = RadioField(choices=[])
