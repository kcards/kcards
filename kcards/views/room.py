from flask import Blueprint, Response, render_template
from flask_api import status, exceptions

from . import api_rooms
from ..models import Room

blueprint = Blueprint('room', __name__, url_prefix='/rooms')


@blueprint.route("/<code>")
def detail(code):
    room = Room.objects(code=code).first()

    if not room:
        raise exceptions.NotFound

    response = Response(render_template("room.html", room=room))

    return response, status.HTTP_200_OK