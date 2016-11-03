# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from kcards.models import Room, Card


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

        @pytest.fixture
        def filled_room(room):
            room.green = ["Bob", "Joe"]
            room.yellow = ["John", "Fred"]
            return room

        def when_empty(room):
            expect(room.queue) == []

        def when_active(filled_room):
            filled_room.active = True

            expect(filled_room.queue) == [
                Card("John", 'yellow'),
                Card("Fred", 'yellow'),
                Card("Bob", 'green'),
                Card("Joe", 'green'),
            ]

        def when_inactive(filled_room):
            filled_room.active = False

            expect(filled_room.queue) == [
                Card("Bob", 'green'),
                Card("John", 'yellow'),
                Card("Fred", 'yellow'),
                Card("Joe", 'green'),
            ]

    def describe_timestamp():

        @pytest.fixture
        def room_with_card(room):
            room.timestamp = 1
            room.green = ["Bob"]
            return room

        def it_starts_at_zero(room):
            expect(room.timestamp) == 0

        def it_increases_when_a_card_is_added(room_with_card):
            room_with_card.add_card("John", 'green')

            expect(room_with_card.timestamp) > 1

        def it_increases_when_a_card_is_removed(room_with_card):
            room_with_card.next_speaker()

            expect(room_with_card.timestamp) > 1

    def describe_add_card():

        def with_single_card(room):
            room.add_card("John Doe", 'green')

            expect(room.queue) == [
                Card("John Doe", 'green'),
            ]

        def with_multiple_cards(room):
            room.add_card("John Doe", 'yellow')
            room.add_card("Jace Browning", 'green')
            room.add_card("Dan Lindeman", 'yellow')

            expect(room.queue) == [
                Card("John Doe", 'yellow'),
                Card("Dan Lindeman", 'yellow'),
                Card("Jace Browning", 'green'),
            ]

        def with_red_card(room):
            room.add_card("John Doe", 'green')
            room.add_card("Jace Browning", 'yellow')
            room.add_card("Dan Lindeman", 'red')

            expect(room.queue) == [
                Card("Dan Lindeman", 'red'),
                Card("John Doe", 'green'),
                Card("Jace Browning", 'yellow'),
            ]

    def describe_next_speaker():

        def it_does_not_remove_from_empty(room):
            room.next_speaker()

            expect(room.queue) == []

        def it_removes_the_red_speaker_first(room):
            room.add_card("John Doe", 'green')
            room.add_card("Jace Browning", 'red')

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", 'green'),
            ]

        def it_starts_a_new_thread(room):
            room.add_card("Jace Browning", 'green')
            room.add_card("John Doe", 'yellow')

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", 'yellow'),
            ]

        def it_removes_the_next_followup(room):
            room.add_card("Jace Browning", 'yellow')
            room.add_card("Dan Lindeman", 'yellow')

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", 'yellow')
            ]

        def it_removes_the_last_followup(room):
            room.add_card("John Doe", 'yellow')
            room.add_card("Jace Browning", 'green')

            room.next_speaker()

            expect(room.queue) == [
                Card("Jace Browning", 'green'),
            ]

        def it_removes_the_current_topic(room):
            room.add_card("John Doe", 'green')
            room.add_card("Jace Browning", 'yellow')
            room.add_card("Dan Lindeman", 'green')

            room.next_speaker()

            expect(room.queue) == [
                Card("Jace Browning", 'yellow'),
                Card("Dan Lindeman", 'green'),
            ]

        def it_removes_the_green_speaker_if_only_greens_are_queued(room):
            room.add_card("John Doe", 'green')
            room.add_card("Dan Lindeman", 'green')

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", 'green'),
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
