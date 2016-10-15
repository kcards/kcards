from flask import Blueprint, url_for
from flask_api import exceptions

from ..models import Room


blueprint = Blueprint('api_rooms', __name__, url_prefix="/api/rooms")


@blueprint.route("/")
def index():
    rooms = sorted(Room.objects)

    links = [url_for('.detail', name=r.name, _external=True) for r in rooms]

    return links


@blueprint.route("/<name>")
def detail(name):
    room = Room.objects(_id=name).first()

    if not room:
        raise exceptions.NotFound

    return room.data
