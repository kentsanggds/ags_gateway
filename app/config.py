# -*- coding: utf-8 -*-
"""
Application configuration
"""

import os


env = os.environ

APP_NAME = env.get('APP_NAME', 'ags_gateway')

DEBUG = bool(env.get('DEBUG', True))

SERVER_NAME = env.get(
    'SERVER_NAME', 'localhost:{}'.format(env.get('PORT', 5000)))

OIDC_CLIENT = {
    'issuer': env.get('OIDC_CLIENT_ISSUER'),
    'client_id': env.get('OIDC_CLIENT_ID'),
    'client_secret': env.get('OIDC_CLIENT_SECRET'),
}

OIDC_PROVIDER = {
    'issuer': env.get(
        'OIDC_PROVIDER_ISSUER', 'https://{}'.format(SERVER_NAME)),
    'subject_id_hash_salt': env.get('SUBJECT_ID_HASH_SALT', 'salt'),
}

PREFERRED_URL_SCHEME = 'https'

VERIFY_SSL = True

# XXX This should be True when served over HTTPS
OIDC_COOKIE_SECURE = False

OIDC_GOOGLE_APPS_DOMAIN = env.get('OIDC_GOOGLE_APPS_DOMAIN')

SECRET_KEY = env.get(
    'SECRET_KEY',
    b'p{\xa7\x18K\rB\x06\xc5\xbdK?\xe5\xdb\xde\x02P\xd0,\x14\xe50\x07\xdd')

# Delay in seconds before redirecting via meta-refresh
META_REFRESH_DELAY = int(env.get('META_REFRESH_DELAY', 7))

# XXX Don't change the following settings unless necessary

# Skips concatenation of bundles if True, which breaks everything
ASSETS_DEBUG = False

ASSETS_LOAD_PATH = [
    'app/static',
    'app/templates']

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(name)s [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'filename': '/tmp/gateway.log',
        }
    },
    'loggers': {
        'app.factory': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'waitress': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
}

WTF_CSRF_ENABLED = True

# TODO this should be True when served via HTTPS
SESSION_COOKIE_SECURE = False
