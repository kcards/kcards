from flask import Blueprint


blueprint = Blueprint('api_rooms', __name__)


@blueprint.route("/api/rooms/")
def index():
    return []
