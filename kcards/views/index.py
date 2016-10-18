from flask import Blueprint, Response, render_template, request

from . import api_rooms

blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def index():
    return Response(render_template("index.html"))


@blueprint.route("/", methods=['POST'])
def create():
    code = request.form['code']
    content, _ = api_rooms.create()
    # return Response(render_template("index.html"))
