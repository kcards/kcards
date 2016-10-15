from flask import Blueprint, request, url_for
from flask_api import status, exceptions

from ..models import Room


blueprint = Blueprint('api_rooms', __name__, url_prefix="/api/rooms")


@blueprint.route("/")
def index():
    rooms = sorted(Room.objects)

    links = [url_for('.detail', code=r.code, _external=True) for r in rooms]

    return links


@blueprint.route("/", methods=['POST'])
def create():
    code = str(request.data.get('code', '')) or None

    room = Room(code).save()

    data = {'uri': url_for('.detail', code=room.code, _external=True)}

    return data, status.HTTP_201_CREATED


@blueprint.route("/<code>")
def detail(code):
    room = Room.objects(_id=code).first()

    if not room:
        raise exceptions.NotFound

    return room.data
