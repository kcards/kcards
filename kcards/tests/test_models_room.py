# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from kcards.models import Room


def describe_room():

    @pytest.fixture
    def room():
        return Room(code='foobar')

    def describe_init():

        def it_generates_an_id_when_unspecified():
            room1 = Room()
            room2 = Room()

            expect(room1) != room2

    def describe_sort():

        def it_uses_the_id():
            rooms = [Room(code='1'), Room(code='A'), Room(code='a')]

            expect(sorted(rooms)) == rooms

    def describe_code():

        def it_matches_the_id(room):
            expect(room.code) == 'foobar'

    def describe_queue():

        def when_empty(room):
            expect(room.queue) == []

        def with_single_card(room):
            room.green.append("John Doe")

            expect(room.queue) == [
                {
                    'color': 'green',
                    'name': "John Doe",
                },
            ]

        def with_multiple_cards(room):
            room.active = True
            room.green.append("John Doe")
            room.yellow.append("Jace Browning")
            room.green.append("Dan Lindeman")

            expect(room.queue) == [
                {
                    'color': 'green',
                    'name': "John Doe",
                },
                {
                    'color': 'green',
                    'name': "Dan Lindeman",
                },
                {
                    'color': 'yellow',
                    'name': "Jace Browning",
                },
            ]

        def with_red_card(room):
            room.active = True
            room.green.append("John Doe")
            room.yellow.append("Jace Browning")
            room.red.append("Dan Lindeman")

            expect(room.queue) == [
                {
                    'color': 'red',
                    'name': "Dan Lindeman",
                },
                {
                    'color': 'green',
                    'name': "John Doe",
                },
                {
                    'color': 'yellow',
                    'name': "Jace Browning",
                },
            ]
