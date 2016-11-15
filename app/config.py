# -*- coding: utf-8 -*-
"""
Application configuration
"""

import os


env = os.environ

APP_NAME = env.get('APP_NAME', 'ags_gateway')

DEBUG = bool(env.get('DEBUG', True))

OIDC_PROVIDERS = {
    'dex': {
        'discovery_url': env.get('OIDC_ISSUER'),
        'client_id': env.get('OIDC_CLIENT_ID'),
        'client_secret': env.get('OIDC_CLIENT_SECRET'),
        'redirect_uri': None
    },
    # 'azure_ad': {
    #     'discovery_url': env.get('OIDC_ISSUER_1'),
    #     'client_id': env.get('OIDC_CLIENT_ID_1'),
    #     'client_secret': env.get('OIDC_CLIENT_SECRET_1'),
    #     'redirect_uri': None
    # },
    # 'google': {
    #     'discovery_url': env.get('OIDC_ISSUER_2'),
    #     'client_id': env.get('OIDC_CLIENT_ID_2'),
    #     'client_secret': env.get('OIDC_CLIENT_SECRET_2'),
    #     'redirect_uri': None
    # }
}

# XXX This should be True when served over HTTPS
OIDC_COOKIE_SECURE = False

OIDC_GOOGLE_APPS_DOMAIN = env.get('OIDC_GOOGLE_APPS_DOMAIN')

SECRET_KEY = env.get(
    'SECRET_KEY',
    b'p{\xa7\x18K\rB\x06\xc5\xbdK?\xe5\xdb\xde\x02P\xd0,\x14\xe50\x07\xdd')

# XXX Don't change the following settings unless necessary

# Skips concatenation of bundles if True, which breaks everything
ASSETS_DEBUG = False

ASSETS_LOAD_PATH = [
    'app/static',
    'app/templates']

# TODO this should be True when served via HTTPS
SESSION_COOKIE_SECURE = False
