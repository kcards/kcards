from flask import Blueprint, Response, render_template, redirect, url_for

from . import api_rooms
from ._utils import call

blueprint = Blueprint('rooms', __name__, url_prefix='/rooms')


@blueprint.route("/")
def index():
    return redirect(url_for('index.get'))


@blueprint.route("/<code>")
def detail(code):
    content, status = call(api_rooms.detail, code)

    if status == 404:
        content = None

    response = Response(render_template("room.html", room=content))

    return response


@blueprint.route("/<code>/next", methods=['POST'])
def next_speaker():
    pass
