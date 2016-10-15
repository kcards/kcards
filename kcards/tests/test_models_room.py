# pylint: disable=unused-variable,unused-argument,expression-not-assigned

import pytest
from expecter import expect

from kcards.models import Room


def describe_room():

    @pytest.fixture
    def room():
        return Room(_id='foobar')

    def describe_code():

        def it_matches_the_id(room):
            expect(room.code) == 'foobar'

    def describe_sorting():

        def it_uses_the_id():
            rooms = [Room('1'), Room('A'), Room('a')]

            expect(sorted(rooms)) == rooms
