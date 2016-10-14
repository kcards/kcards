from flask import Blueprint, Response, render_template


blueprint = Blueprint('room', __name__)


@blueprint.route("/rooms/<key>")
def detail(key):
    # Placeholder for how to 404 when a room is not in the room list.
    if key is 'not_found':
        key=None
    return Response(render_template("room.html", key=key))