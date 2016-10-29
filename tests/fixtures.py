# pylint: disable=redefined-outer-name

import pytest

from kcards.app import create_app
from kcards.settings import get_config
from kcards import models


@pytest.fixture
def app():
    return create_app(get_config('test'))


@pytest.fixture
def client(app):
    models.Room.objects.delete()
    return app.test_client()


@pytest.fixture
def room():
    room = models.Room(code='foobar')
    room.save()
    return room


@pytest.fixture
def populated_room(room):
    room.add("John Doe", 'green')
    room.save()
    return room
