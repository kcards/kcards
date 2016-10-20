from flask import Blueprint, Response, render_template
from flask_api import exceptions

from . import api_rooms

blueprint = Blueprint('room', __name__, url_prefix='/rooms')


@blueprint.route("/<code>")
def detail(code):
    try:
        content, _ = api_rooms.detail(code)
    except exceptions.NotFound:
        content = None

    response = Response(render_template("room.html", room=content))

    return response


@blueprint.route("/<code>/next", methods=['POST'])
def next_speaker():
    pass
