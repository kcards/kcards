from flask import Blueprint, Response, render_template
from flask_api import exceptions

from . import api_rooms

blueprint = Blueprint('room', __name__, url_prefix='/rooms')


@blueprint.route("/<code>")
def detail(code):
    try:
        content, _ = api_rooms.detail(code)
    except exceptions.NotFound:
        room_code = None
    else:
        room_code = content['code']

    response = Response(render_template("room.html", code=room_code))
    return response
