from flask import (Blueprint, Response,
                   request, render_template, redirect, url_for)

from . import api_rooms
from ._utils import call


blueprint = Blueprint('rooms', __name__, url_prefix="/rooms")


@blueprint.route("/")
def index():
    return redirect(url_for('index.get'))


@blueprint.route("/<code>")
def detail(code):
    name = request.args.get('name')
    content, status = call(api_rooms.detail, code)

    if status == 404:
        content = None
    elif not name:
        return redirect(url_for('join.get', code=content['code']))

    response = Response(render_template("room.html", room=content, name=name))

    return response


@blueprint.route("/<code>", methods=['POST'])
def update(code):
    name = request.args['name']

    if 'next' in request.form:
        content, _ = call(api_rooms.next_speaker, code=code)

    else:
        if 'new' in request.form:
            color = 'green'
        elif 'follow' in request.form:
            color = 'yellow'
        elif 'interrupt' in request.form:
            color = 'red'

        content, _ = call(api_rooms.queue, code=code, name=name, color=color)

    response = Response(render_template("room.html", room=content, name=name))

    return response
