from flask import Blueprint, url_for
from flask_api import status


blueprint = Blueprint('api_root', __name__)


@blueprint.route("/api")
def index():
    content = {'rooms': url_for('api_rooms.index', _external=True)}

    return content, status.HTTP_200_OK
