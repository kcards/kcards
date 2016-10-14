from flask import Blueprint, url_for


blueprint = Blueprint('api_root', __name__)


@blueprint.route("/api")
def index():
    return {'rooms': url_for('api_rooms.index', _external=True)}
