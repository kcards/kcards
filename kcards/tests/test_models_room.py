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

    def describe_next_speaker():

        def it_does_not_remove_from_empty(room):
            room.next_speaker()
            expect(room.queue) == []

        # def it_removes_the_green_speaker_on_new_thread(room):
        #     room.add("Jace Browning", 'green')
        #     room.add("John Doe", 'yellow')
        #     room.next_speaker()
        #     expect(room.queue) == [
        #         {
        #             'name': "Jace Browning",
        #             'color': 'green',
        #         },
        #     ]

        # def it_removes_the_yellow_speaker_on_current_thread(room):
        #     room.add("John Doe", 'yellow')
        #     room.add("Jace Browning", 'green')
        #     room.next_speaker()
        #     expect(room.queue) == [
        #         {
        #             'name': "John Doe",
        #             'color': 'yellow',
        #         },
        #     ]

        # def it_removes_the_yellow_speaker_if_another_green_is_queued(room):
        #     room.add("John Doe", 'green')
        #     room.add("Jace Browning", 'yellow')
        #     room.add("Dan Lindeman", 'green')
        #     room.next_speaker()
        #     expect(room.queue) == [
        #         {
        #             'name': "John Doe",
        #             'color': 'green',
        #         },
        #         {
        #             'name': "Dan Lindeman",
        #             'color': 'green',

        #         },
        #     ]

        # def it_removes_the_green_speaker_if_only_greens_are_queued(room):
        #     room.add("John Doe", 'green')
        #     room.add("Dan Lindeman", 'green')
        #     room.next_speaker()
        #     expect(room.queue) == [
        #         {
        #             'name': "Dan Lindeman",
        #             'color': 'green',

        #         },
        #     ]

        def it_removes_the_red_speaker(room):
            room.add("John Doe", 'green')
            room.add("Jace Browning", 'red')
            room.next_speaker()
            expect(room.queue) == [
                {
                    'name': "John Doe",
                    'color': 'green',
                }
            ]

    def describe_queue():

        def when_empty(room):
            expect(room.queue) == []

        def with_single_card(room):
            room.add("John Doe", 'green')

            expect(room.queue) == [
                {
                    'name': "John Doe",
                    'color': 'green',
                },
            ]

        def with_multiple_cards(room):
            room.add("John Doe", 'yellow')
            room.add("Jace Browning", 'green')
            room.add("Dan Lindeman", 'yellow')

            expect(room.queue) == [
                {
                    'name': "John Doe",
                    'color': 'yellow',
                },
                {
                    'name': "Dan Lindeman",
                    'color': 'yellow',

                },
                {
                    'name': "Jace Browning",
                    'color': 'green',
                },
            ]

        def with_red_card(room):
            room.add("John Doe", 'green')
            room.add("Jace Browning", 'yellow')
            room.add("Dan Lindeman", 'red')

            expect(room.queue) == [
                {
                    'name': "Dan Lindeman",
                    'color': 'red',
                },
                {
                    'name': "John Doe",
                    'color': 'green',
                },
                {
                    'name': "Jace Browning",
                    'color': 'yellow',
                },
            ]
