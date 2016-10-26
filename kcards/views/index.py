from flask import Blueprint, Response, render_template, redirect, url_for, flash

from . import api_rooms

from . import _exceptions as exceptions

blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def index():
    return Response(render_template("index.html"))


@blueprint.route("/", methods=['POST'])
def create():
    try:
        content, _ = api_rooms.create()
    except exceptions.Conflict:
        flash("Room already exists.")
        return redirect(url_for('.index'))
    else:
        return redirect(url_for('room.detail', code=content['code']))
