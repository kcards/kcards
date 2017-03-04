import time
import logging

from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Room, Color

from . import _exceptions as exceptions
from ._utils import get_content


blueprint = Blueprint('api_rooms', __name__, url_prefix="/api/rooms")
log = logging.getLogger(__name__)


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

    return get_content(room), status.HTTP_201_CREATED


@blueprint.route("/", methods=['DELETE'])
def cleanup():
    content = [room.code for room in Room.cleanup()]

    return content, status.HTTP_200_OK


@blueprint.route("/<code>")
def detail(code):
    cleaned_code = Room.clean_code(code)
    room = Room.objects(code=cleaned_code).first()

    if not room:
        raise exceptions.NotFound(f"Room not found: {code}")

    return get_content(room), status.HTTP_200_OK


@blueprint.route("/<code>/timestamp")
def timestamp(code):
    current_timestamp = int(request.args.get('current', 0))

    room = Room.objects(code=code).first()
    if not room:
        return dict(timestamp=0)

    if current_timestamp:
        log.debug("Waiting for timestamp change from %s...", current_timestamp)
        start_time = time.time()
        while room.timestamp == current_timestamp:
            elapsed_time = time.time() - start_time
            if elapsed_time > 20:
                log.debug("No timestamp change prior to timeout")
                break
            room.reload('timestamp')
        else:
            log.debug("New timestamp: %s", room.timestamp)

    return dict(timestamp=room.timestamp)


@blueprint.route("/<code>/queue", methods=['GET', 'POST'])
def queue(code, name=None, color=None):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound("This room could not be found.")

    if request.method == 'GET':
        return get_content(room), status.HTTP_200_OK

    try:
        name = name or request.data['name']
        color = color or Color[request.data['color']]
    except KeyError as exc:
        log.debug(exc)
        raise exceptions.UnprocessableEntity("Name and color are required.")

    room.add_card(name, color)
    room.save()

    return get_content(room), status.HTTP_200_OK


@blueprint.route("/<code>/queue", methods=['DELETE'])
def clear(code):
    log.info("Clearing the %r room queue", code)

    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound

    room.clear_queue()
    room.save()

    return get_content(room), status.HTTP_200_OK


@blueprint.route("/<code>/next", methods=['GET', 'POST'])
def next_speaker(code, name=None, force=False):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound

    if request.method == 'GET':
        return get_content(room), status.HTTP_200_OK

    try:
        name = name or request.data['name']
    except KeyError as exc:
        log.debug(exc)
        raise exceptions.UnprocessableEntity("Name required.")

    if not room.queue:
        return get_content(room), status.HTTP_200_OK

    if room.queue[0]['name'] == name or force:
        room.next_speaker()

    room.save()
    return get_content(room), status.HTTP_200_OK


@blueprint.route("/<code>", methods=['DELETE'])
def delete(code):
    log.info("Deleting %r room", code)
    room = Room.objects(code=code).first()

    if room:
        room.delete()

    return '', status.HTTP_204_NO_CONTENT
