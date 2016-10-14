from flask import Blueprint, Response, render_template


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def index():
    return Response(render_template("index.html"))
