from flask import Blueprint, Response, render_template, redirect, url_for

from . import api_rooms

blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def index():
    return Response(render_template("index.html"))


@blueprint.route("/", methods=['POST'])
def create():
    content, _ = api_rooms.create()

    return redirect(url_for('room.detail', code=content['code']))
