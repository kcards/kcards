# pylint: disable=redefined-outer-name

import pytest

from kcards.app import create_app
from kcards.settings import get_config
from kcards.models import Room, Color


@pytest.fixture
def app():
    return create_app(get_config('test'))


@pytest.fixture
def client(app):
    Room.objects.delete()
    return app.test_client()


@pytest.fixture
def room():
    room = Room(code='foobar')
    room.save()
    return room


@pytest.fixture
def populated_room(room):
    room.add_card("John Doe", Color.change)
    room.save()
    return room
