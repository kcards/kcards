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
    requested_code = request.form.get('code', "").strip()
    content = None
    status = None

    if 'goto' in request.form and requested_code:
        content, status = call(api_rooms.detail, code=requested_code)

    elif 'create' in request.form:
        content, status = call(api_rooms.create)

    if status and status >= 400:
        flash(content['message'], 'error')
        return redirect(url_for('.get'))

    if not requested_code:
        flash("Room code is required.", 'error')
        return redirect(url_for('.get'))

    return redirect(url_for('rooms.detail', code=content['code']))
