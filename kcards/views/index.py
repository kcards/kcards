from flask import (Blueprint, Response,
                   render_template, request, redirect, url_for, flash)

from . import api_rooms
from ._utils import call

blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def get():
    return Response(render_template("index.html"))


@blueprint.route("/", methods=['POST'])
def create():
    code = None

    if 'join' in request.form:
        code = request.form.get('code')

    elif 'create' in request.form:
        content, status = call(api_rooms.create)

        if status == 409:
            flash(content['message'])
            return redirect(url_for('.get'))
        else:
            code = content['code']

    if not code:
        flash("Room code is required.")
        return redirect(url_for('.get'))

    return redirect(url_for('rooms.detail', code=code))
