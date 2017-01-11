import json
import time
from urllib.parse import urlparse

from jwkest import jws
from jwkest.jwk import RSAKey, rsa_load
from oic import rndstr
from oic.oic import Server
from oic.oic.message import (
    AccessTokenResponse,
    AuthorizationResponse,
    EndSessionResponse,
    IdToken,
    OpenIDSchema,
)
import responses


class MockOIDCProvider(Server):

    def __init__(self, config={}):
        Server.__init__(self)
        self.session = None
        self.config = {
            'issuer': 'https://example.com',
        }
        self.config.update(config)
        self.authz_codes = {}
        self.access_tokens = {}
        self.client = {
            'test-client': {
                'client_name': 'Test Client',
                'client_secret': 'test-secret',
                'post_logout_redirect_uris': [
                    'http://localhost:5000/sign-out',
                ],
                'redirect_uris': [
                    'http://localhost:5000/oidc_callback',
                ],
                'response_types': ['code'],
            }
        }
        self.access_token_lifetime = 3600
        self.authorization_code_lifetime = 600
        self.id_token_lifetime = 3600
        self.registration_expires_in = 3600
        self.host = ''
        self.userinfo_signed_response_alg = ''
        self.signing_key = RSAKey(key=rsa_load('signing_key.pem'), alg='RS256')

    def __enter__(self):
        self.patch = responses.RequestsMock(
            assert_all_requests_are_fired=False)
        self.patch.start()
        self.init_endpoints()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.patch.stop()
        return False

    @property
    def calls(self):
        return self.patch.calls

    def init_endpoints(self):

        url = '{issuer}/.well-known/openid-configuration'.format(**self.config)
        self.openid_configuration = MockProviderConfig(url, self)

        url = '{issuer}/keys'.format(**self.config)
        self.jwks_uri = MockJwks(url, self)

        url = '{issuer}/auth'.format(**self.config)
        self.authorization_endpoint = MockAuthorizationEndpoint(url, self)

        url = '{issuer}/token'.format(**self.config)
        self.token_endpoint = MockTokenEndpoint(url, self)

        url = '{issuer}/userinfo'.format(**self.config)
        self.userinfo_endpoint = MockUserinfoEndpoint(url, self)

        url = '{issuer}/logout'.format(**self.config)
        self.end_session_endpoint = MockEndSessionEndpoint(url, self)


class MockEndpoint(object):
    method = responses.GET

    def __init__(self, url, provider):
        self.url = url
        self.provider = provider
        self.config = self.provider.config
        self.provider.patch.add_callback(self.method, self.url, self)

    @property
    def calls(self):
        return [
            call for call in self.provider.patch.calls
            if call.request.url.startswith(self.url)]

    @property
    def called(self):
        return len(self.calls) > 0


class MockProviderConfig(MockEndpoint):

    def __call__(self, request):
        config = {
            'issuer': self.config['issuer'],
            'authorization_endpoint': '{issuer}/auth'.format(**self.config),
            'jwks_uri': '{issuer}/keys'.format(**self.config),
            'token_endpoint': '{issuer}/token'.format(**self.config),
            'userinfo_endpoint': '{issuer}/userinfo'.format(**self.config),
            'registration_endpoint': '{issuer}/register'.format(**self.config),
            'end_session_endpoint': '{issuer}/signout'.format(**self.config),
            'scopes_supported': ['openid', 'profile'],
            'response_types_supported': [
                'code', 'code id_token', 'code token', 'code id_token token'],
            'response_modes_supported': ['query', 'fragment'],
            'grant_types_supported': ['authorization_code', 'implicit'],
            'subject_types_supported': ['pairwise'],
            'token_endpoint_auth_methods_supported': ['client_secret_basic'],
            'claims_parameter_supported': True
        }
        return (200, {'Content-Type': 'application/json'}, json.dumps(config))


class MockJwks(MockEndpoint):

    def __call__(self, request):
        keys = {'keys': [self.provider.signing_key.serialize()]}
        return (200, {'Content-Type': 'application/json'}, json.dumps(keys))


class MockAuthorizationEndpoint(MockEndpoint):

    def __call__(self, request):
        query = urlparse(request.url).query

        req = self.provider.parse_authorization_request(query=query)

        resp = AuthorizationResponse()

        if 'code' in req['response_type']:
            authz_code = rndstr(10)
            authz_info = {
                'used': False,
                'exp': time.time() + self.provider.authorization_code_lifetime,
                'sub': 'test-sub',
                'granted_scope': ' '.join(req['scope']),
                'auth_req': req.to_dict()
            }
            self.provider.authz_codes[authz_code] = authz_info

            resp['code'] = authz_code

        if 'state' in req:
            resp['state'] = req['state']

        return (302, {'Location': resp.request(req['redirect_uri'])}, '')


class MockTokenEndpoint(MockEndpoint):
    method = responses.POST

    def __call__(self, request):
        data = request.body

        req = self.provider.parse_token_request(body=data)

        if 'grant_type' not in req:
            return (400, {}, 'Missing grant_type')

        if req['grant_type'] == 'authorization_code':
            authz_code = req['code']
            authz_info = self.provider.authz_codes[authz_code]
            auth_req = authz_info['auth_req']
            client_id = auth_req['client_id']

            if authz_info['used']:
                raise Exception('code already used')
                return (400, {}, 'Invalid authorization code')

            if authz_info['exp'] < time.time():
                raise Exception('code expired')
                return (400, {}, 'Invalid authorization code')

            authz_info['used'] = True

            access_token = {
                'value': rndstr(),
                'expires_in': self.provider.access_token_lifetime,
                'type': 'Bearer'
            }

            at_value = access_token['value']

            self.provider.access_tokens[at_value] = {
                'iat': time.time(),
                'exp': time.time() + self.provider.access_token_lifetime,
                'sub': 'test-sub',
                'client_id': client_id,
                'aud': [client_id],
                'scope': authz_info['granted_scope'],
                'granted_scope': authz_info['granted_scope'],
                'token_type': access_token['type'],
                'auth_req': auth_req
            }

            resp = AccessTokenResponse()
            resp['access_token'] = at_value
            resp['token_type'] = access_token['type']
            resp['expires_in'] = access_token['expires_in']

            resp['refresh_token'] = None

            args = {
                'c_hash': jws.left_hash(authz_code.encode('utf-8'), 'HS256'),
                'at_hash': jws.left_hash(at_value.encode('utf-8'), 'HS256'),
            }

            id_token = IdToken(
                iss=self.config['issuer'],
                sub='test-sub',
                aud=client_id,
                iat=time.time(),
                exp=time.time() + self.provider.id_token_lifetime,
                **args)

            if 'nonce' in auth_req:
                id_token['nonce'] = auth_req['nonce']

            resp['id_token'] = id_token.to_jwt(
                [self.provider.signing_key], 'RS256')

            json_data = resp.to_json()

            return (
                200,
                {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-store',
                    'Pragma': 'no-cache',
                },
                json_data
            )

        return (400, {}, 'Unsupported grant_type')


class MockUserinfoEndpoint(MockEndpoint):
    method = responses.POST

    def __call__(self, request):
        data = request.body

        self.provider.parse_user_info_request(data)

        _info = {
            'sub': 'test-sub',
            'name': 'Test User',
            'nickname': 'Tester',
            'email': 'tester@example.com',
            'verified': True,
        }

        resp = OpenIDSchema(**_info)

        userinfo = resp.to_json()

        return (200, {'Content-Type': 'application/json'}, userinfo)


class MockEndSessionEndpoint(MockEndpoint):

    def __call__(self, request):
        query = urlparse(request.url).query
        req = self.provider.parse_end_session_request(query=query)

        resp = EndSessionResponse(state=req['state'])

        return (302, {'Location': resp.request(req['redirect_url'])}, '')
