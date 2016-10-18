from flask import Blueprint, Response, render_template, request, redirect, url_for

from . import api_rooms

blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def index():
    return Response(render_template("index.html"))


@blueprint.route("/", methods=['POST'])
def create():
    content, _ = api_rooms.create()
    # TODO: this is a temporary hack
    # we should probably return code in both GET /rooms/X and POST /rooms
    code = content['uri'].split('/')[-1]

    return redirect(url_for('room.detail', code=code))
