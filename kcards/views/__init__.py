from flask import request
from flask_nav.elements import Navbar, View as _View, Text

from ..extensions import nav

from . import index
from . import rooms
from . import join
from . import options
from . import api_root
from . import api_rooms


class View(_View):
    """Workaround for https://github.com/mbr/flask-nav/issues/17."""

    @property
    def active(self):
        return request.full_path == self.get_url()


@nav.navigation()
def top():
    code = request.view_args.get('code')
    name = request.args.get('name')

    lobby = View("lobby", 'index.get')
    room = View(code, 'rooms.detail', code=code, name=name)
    page = Text(request.path.split('/')[-1])
    page.active = True

    if code:
        if page.text in ['join', 'options']:
            items = [lobby, room, page]
        else:
            items = [lobby, room]
    else:
        items = [lobby]

    return Navbar("K-Cards", *items)
