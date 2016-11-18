from flask import Response


class AuthenticationRequestError(Response, Exception):
    default_status = 400


class AuthenticationRequest(object):

    def __init__(self, request):
        self.request = request

        if 'error' in request.args:
            raise AuthenticationRequestError('Error')

    @property
    def specific_idp(self):
        if 'specific' in self.request.args:
            return 'google'

    @property
    def suggested_idp(self):
        if 'suggested' in self.request.args:
            return 'google'
