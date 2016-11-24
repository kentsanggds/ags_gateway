# -*- coding: utf-8 -*-
"""
AGS Gateway app factory
"""

import os

from flask import Flask, render_template


def create_app(config='config.py', **kwargs):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    app.config.update(kwargs)

    register_blueprints(app)
    register_context_processors(app)
    register_error_handlers(app)
    register_extensions(app)

    return app


def register_blueprints(app):

    from app.main import main
    app.register_blueprint(main)

    from app.oidc_provider import oidc_provider
    app.register_blueprint(oidc_provider)


def register_context_processors(app):

    def base_context_processor():
        return {
            'asset_path': '/static/govuk_template/assets/',
        }

    app.context_processor(base_context_processor)


def register_error_handlers(app):

    error_handlers = {
        '404.html': [404],
        # avoid flask 0.11 bug with 402 and 407
        '4xx.html': [401, 405, 406, 408, 409],
        '5xx.html': [500, 501, 502, 503, 504, 505]}

    def make_handler(code, template):
        template = os.path.join('errors', template)

        def handler(e):
            return render_template(template, code=code), code

        return handler

    for template, codes in error_handlers.items():
        for code in codes:
            app.register_error_handler(code, make_handler(code, template))


def register_extensions(app):

    from app.assets import env
    env.init_app(app)

    from app.oidc_provider import init_oidc_provider
    app.provider = init_oidc_provider(app)
