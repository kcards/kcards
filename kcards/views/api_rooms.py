from flask import Blueprint, request, url_for
from flask_api import status, exceptions

from ..models import Room


blueprint = Blueprint('api_rooms', __name__, url_prefix="/api/rooms")


@blueprint.route("/")
def index():
    rooms = sorted(Room.objects)

    content = [url_for('.detail', code=r.code, _external=True) for r in rooms]

    return content, status.HTTP_200_OK


@blueprint.route("/", methods=['POST'])
def create():
    code = str(request.data.get('code', '')) or None
    room = Room(code=code).save()

    content = {'uri': url_for('.detail', code=room.code, _external=True)}

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

    return room.data, status.HTTP_200_OK


@blueprint.route("/<code>/queue", methods=['GET', 'POST'])
def queue(code):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound

    if request.method == 'GET':
        return room.queue, status.HTTP_200_OK

    color = request.data['color']
    name = request.data['name']

    getattr(room, color).append(name)
    room.save()

    return room.queue, status.HTTP_202_ACCEPTED
