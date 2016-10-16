from flask import Blueprint, Response, render_template
from flask_api import exceptions

from . import api_rooms


blueprint = Blueprint('room', __name__)


@blueprint.route("/rooms/<code>")
def detail(code):
    try:
        room, _ = api_rooms.detail(code)
    except exceptions.NotFound:
        room = None

    return Response(render_template("room.html", room=room))
