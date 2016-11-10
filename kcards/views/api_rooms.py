from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Room, Color

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
        raise exceptions.Conflict("Room already exists.")

    room = Room(code=code).save()

    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    return content, status.HTTP_201_CREATED


@blueprint.route("/", methods=['DELETE'])
def cleanup():
    content = [room.code for room in Room.cleanup()]

    return content, status.HTTP_200_OK


@blueprint.route("/<code>")
def detail(code):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound

    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    return content, status.HTTP_200_OK


@blueprint.route("/<code>/timestamp")
def timestamp(code):
    room = Room.objects(code=code).first()

    return dict(timestamp=room.timestamp if room else 0)


@blueprint.route("/<code>/next", methods=['GET', 'POST'])
def next_speaker(code):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound

    # TODO: clean up this redundancy
    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    if request.method == 'GET':
        return content, status.HTTP_200_OK

    room.next_speaker()
    room.save()

    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    return content, status.HTTP_200_OK


@blueprint.route("/<code>/queue", methods=['GET', 'POST'])
def queue(code, name=None, color=None):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound("This room could not be found.")

    # TODO: clean up this redundancy
    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    if request.method == 'GET':
        return content, status.HTTP_200_OK

    name = name or request.data['name']
    color = color or Color[request.data['color']]
    room.add_card(name, color)
    room.save()

    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)

    return content, status.HTTP_200_OK


@blueprint.route("/<code>", methods=['DELETE'])
def delete(code):
    room = Room.objects(code=code).first()

    if room:
        room.delete()

    return '', status.HTTP_204_NO_CONTENT
