from flask import url_for
from flask_api.exceptions import APIException


def call(function, *args, **kwargs):
    """Call the API internally."""
    try:
        content, status = function(*args, **kwargs)
    except APIException as exc:
        content = {'message': exc.detail}
        status = exc.status_code
    return content, status


def get_content(room):
    """Serialize a room for API responses."""
    content = room.data
    content['uri'] = url_for('api_rooms.detail', code=room.code, _external=True)
    return content
