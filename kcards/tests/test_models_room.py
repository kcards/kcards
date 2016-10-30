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

    def describe_add_card():

        def with_single_card(room):
            room.add_card("John Doe", 'green')

            expect(room.queue) == [
                {
                    'name': "John Doe",
                    'color': 'green',
                },
            ]

        def with_multiple_cards(room):
            room.add_card("John Doe", 'yellow')
            room.add_card("Jace Browning", 'green')
            room.add_card("Dan Lindeman", 'yellow')

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
            room.add_card("John Doe", 'green')
            room.add_card("Jace Browning", 'yellow')
            room.add_card("Dan Lindeman", 'red')

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

    def describe_next_speaker():

        def it_does_not_remove_from_empty(room):
            room.next_speaker()
            expect(room.queue) == []

        def it_starts_a_new_thread(room):
            room.add_card("Jace Browning", 'green')
            room.add_card("John Doe", 'yellow')
            room.next_speaker()
            expect(room.queue) == [
                {
                    'name': "John Doe",
                    'color': 'yellow',
                },
            ]

        def it_removes_the_last_followup(room):
            room.add_card("John Doe", 'yellow')
            room.add_card("Jace Browning", 'green')
            room.next_speaker()
            expect(room.queue) == [
                {
                    'name': "Jace Browning",
                    'color': 'green',
                },
            ]

        def it_removes_current_topic(room):
            room.add_card("John Doe", 'green')
            room.add_card("Jace Browning", 'yellow')
            room.add_card("Dan Lindeman", 'green')
            room.next_speaker()
            expect(room.queue) == [
                {
                    'name': "Jace Browning",
                    'color': 'yellow',
                },
                {
                    'name': "Dan Lindeman",
                    'color': 'green',

                },
            ]

        def it_removes_the_green_speaker_if_only_greens_are_queued(room):
            room.add_card("John Doe", 'green')
            room.add_card("Dan Lindeman", 'green')
            room.next_speaker()
            expect(room.queue) == [
                {
                    'name': "Dan Lindeman",
                    'color': 'green',

                },
            ]

        def it_clears_the_queue_without_active_discussion(room):
            room.add_card("John Doe", 'green')
            room.add_card("Dan Lindeman", 'green')
            room.next_speaker()
            room.next_speaker()
            expect(room.queue) == []

        def it_clears_the_queue_with_active_discussion(room):
            room.add_card("John Doe", 'green')
            room.add_card("Jace Browning", 'yellow')
            room.add_card("Dan Lindeman", 'green')
            room.next_speaker()
            room.next_speaker()
            room.next_speaker()
            expect(room.queue) == []

        def it_removes_the_red_speaker(room):
            room.add_card("John Doe", 'green')
            room.add_card("Jace Browning", 'red')
            room.next_speaker()
            expect(room.queue) == [
                {
                    'name': "John Doe",
                    'color': 'green',
                }
            ]
