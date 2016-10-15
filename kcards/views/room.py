from flask import Blueprint, Response, render_template


blueprint = Blueprint('room', __name__)


@blueprint.route("/rooms/<code>")
def detail(code):
    # Placeholder for how to 404 when a room is not in the room list.
    # if code is None:
    if code == 'not_found':
        code = None
    return Response(render_template("room.html", room=code))
