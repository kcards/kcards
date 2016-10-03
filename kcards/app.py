import logging

from flask import Flask

from . import views


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    configure_logging(app)

    register_blueprints(app)

    return app


def configure_logging(app):
    if app.config['DEBUG']:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def register_blueprints(app):
    app.register_blueprint(views.index.blueprint)
