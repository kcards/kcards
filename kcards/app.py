import logging

from flask_api import FlaskAPI

from . import views
from . import extensions


log = logging.getLogger(__name__)


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
    app.register_blueprint(views.rooms.blueprint)
    app.register_blueprint(views.join.blueprint)
    app.register_blueprint(views.options.blueprint)


def register_extensions(app):
    extensions.db.init_app(app)
    extensions.bootstrap.init_app(app)
    extensions.nav.init_app(app)
