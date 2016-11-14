from flask import (Blueprint, Response,
                   request, redirect, url_for, render_template)

from ._utils import call
from .import api_rooms


blueprint = Blueprint('options', __name__, url_prefix="/rooms")


@blueprint.route("/<code>/options")
def index(code):
    return Response(render_template("options.html", code=code))


@blueprint.route("/<code>/options", methods=['POST'])
def action(code):
    name = request.args['name']

    if 'clear' in request.form:
        call(api_rooms.clear, code)

    elif 'delete' in request.form:
        call(api_rooms.delete, code)

    return redirect(url_for('rooms.detail', code=code, name=name))
