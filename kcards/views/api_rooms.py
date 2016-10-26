from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Room

from . import _exceptions as exceptions


blueprint = Blueprint('api_rooms', __name__, url_prefix="/api/rooms")


@blueprint.route("/")
def index():
    rooms = sorted(Room.objects)

    content = [url_for('api_rooms.detail', code=room.code, _external=True)
               for room in rooms]

    return content, status.HTTP_200_OK


@blueprint.route("/", methods=['POST'])
def create():
    code = str(request.data.get('code', '')) or None

    existing = Room.objects(code=code).first()
    if existing:
        raise exceptions.Conflict("This room already exists.")

    room = Room(code=code).save()

    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    return content, status.HTTP_201_CREATED


@blueprint.route("/<code>", methods=['DELETE'])
def delete(code):
    room = Room.objects(code=code).first()

    if room:
        room.delete()

    return '', status.HTTP_204_NO_CONTENT


@blueprint.route("/<code>")
def detail(code):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound

    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    return content, status.HTTP_200_OK


@blueprint.route("/<code>/queue", methods=['GET', 'POST'])
def queue(code):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound("This room could not be found.")

    # TODO: clean up this redundancy
    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    if request.method == 'GET':
        return content, status.HTTP_200_OK

    color = request.data['color']
    name = request.data['name']

    getattr(room, color).append(name)
    room.save()

    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    return content, status.HTTP_202_ACCEPTED
