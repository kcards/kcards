import logging

from flask_api import FlaskAPI

from . import views
from . import extensions


def create_app(config):
    app = FlaskAPI(__name__)
    app.config.from_object(config)

    configure_logging(app)

    register_blueprints(app)
    register_extensions(app)

    return app


def configure_logging(app):
    if app.config['DEBUG']:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def register_blueprints(app):
    register_backend(app)
    register_frontend(app)


def register_backend(app):
    app.register_blueprint(views.api_root.blueprint)
    app.register_blueprint(views.api_rooms.blueprint)


def register_frontend(app):
    app.register_blueprint(views.index.blueprint)
    app.register_blueprint(views.room.blueprint)


def register_extensions(app):
    extensions.mongo.init_app(app)
