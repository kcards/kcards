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
    return app.test_client()


@pytest.fixture
def room():
    room = models.Room(_id='foobar')
    room.save()
