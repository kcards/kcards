from flask import request
from flask_nav.elements import Navbar, View, Text

from ..extensions import nav

from . import index
from . import rooms
from . import join
from . import options
from . import api_root
from . import api_rooms


@nav.navigation()
def top():
    code = request.view_args.get('code')
    name = request.args.get('name')

    lobby = View("lobby", 'index.get')
    room = View(code, 'rooms.detail', code=code, name=name)
    _page_name = request.path.split('/')[-1]
    _page_endpoint = request.url_rule.endpoint
    page = View(_page_name, _page_endpoint, code=code)

    if code:
        if page.text in ['join', 'options']:
            items = [lobby, room, page]
        else:
            items = [lobby, room]
    else:
        items = [lobby]

    return Navbar("K-Cards", *items)
