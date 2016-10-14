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
    app.register_blueprint(views.api_root.blueprint)
    app.register_blueprint(views.api_rooms.blueprint)
    app.register_blueprint(views.index.blueprint)


def register_extensions(app):
    extensions.db.init_app(app)
