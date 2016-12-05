# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect
from freezegun import freeze_time

from kcards.models import Room, Card, Color


def describe_room():

    @pytest.fixture
    @freeze_time("2016-11-09 9:33:12")
    def room():
        return Room(code='foobar')

    def describe_init():

        def it_generates_a_unique_code_when_unspecified():
            room1 = Room()
            room2 = Room()

            expect(room1) != room2

        def it_allows_custom_codes():
            room = Room(code='1234')

            expect(room.code) == '1234'

    def describe_sort():

        def it_uses_the_id():
            rooms = [Room(code='1'), Room(code='A'), Room(code='a')]

            expect(sorted(rooms)) == rooms

    def describe_clean_code():
        def it_converts_to_lowercase():
            room = Room(code='Foobar')

            room.clean()

            expect(room.code) == 'foobar'

        def it_replaces_spaces_with_dashes():
            room = Room(code=' with spaces  here')

            room.clean()

            expect(room.code) == 'with-spaces-here'

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
                Card("John", Color.yellow),
                Card("Fred", Color.yellow),
                Card("Bob", Color.green),
                Card("Joe", Color.green),
            ]

        def when_inactive(filled_room):
            filled_room.active = False

            expect(filled_room.queue) == [
                Card("Bob", Color.green),
                Card("John", Color.yellow),
                Card("Fred", Color.yellow),
                Card("Joe", Color.green),
            ]

    def describe_timestamp():

        @pytest.fixture
        def room_with_card(room):
            room.timestamp = 1
            room.green = ["Bob"]
            return room

        def it_starts_at_the_current_time(room):
            expect(room.timestamp) == 1478683992

        def it_increases_when_a_card_is_added(room_with_card):
            old_timestamp = room_with_card.timestamp

            room_with_card.add_card("John", Color.green)

            expect(room_with_card.timestamp) > old_timestamp

        def it_increases_when_a_card_is_removed(room_with_card):
            old_timestamp = room_with_card.timestamp

            room_with_card.next_speaker()

            expect(room_with_card.timestamp) > old_timestamp

    def describe_add_card():

        def with_single_card(room):
            room.add_card("John Doe", Color.green)

            expect(room.queue) == [
                Card("John Doe", Color.green),
            ]

        def with_multiple_cards(room):
            room.add_card("John Doe", Color.yellow)
            room.add_card("Jace Browning", Color.green)
            room.add_card("Dan Lindeman", Color.yellow)

            expect(room.queue) == [
                Card("John Doe", Color.yellow),
                Card("Dan Lindeman", Color.yellow),
                Card("Jace Browning", Color.green),
            ]

        def with_red_card(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Jace Browning", Color.yellow)
            room.add_card("Dan Lindeman", Color.red)

            expect(room.queue) == [
                Card("Dan Lindeman", Color.red),
                Card("John Doe", Color.green),
                Card("Jace Browning", Color.yellow),
            ]

    def describe_next_speaker():

        def it_leaves_empty_rooms_unchanged(room):
            room.next_speaker()

            expect(room.queue) == []

        def it_removes_interrupts_first(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Jace Browning", Color.red)

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", Color.green),
            ]

        def it_can_start_a_new_thread(room):
            room.add_card("Jace Browning", Color.green)
            room.add_card("John Doe", Color.yellow)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", Color.yellow),
                Card("Dan Lindeman", Color.green),
            ]

        def it_removes_the_next_followup(room):
            room.add_card("Jace Browning", Color.yellow)
            room.add_card("Dan Lindeman", Color.yellow)

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", Color.yellow)
            ]

        def it_removes_the_last_followup(room):
            room.add_card("John Doe", Color.yellow)
            room.add_card("Jace Browning", Color.green)

            room.next_speaker()

            expect(room.queue) == [
                Card("Jace Browning", Color.green),
            ]

        def it_can_advance_to_the_next_topic(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", Color.green),
            ]

        def it_clears_the_queue_without_active_discussion(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()
            room.next_speaker()

            expect(room.queue) == []

        def it_clears_the_queue_with_active_discussion(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Jace Browning", Color.yellow)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()
            room.next_speaker()
            room.next_speaker()

            expect(room.queue) == []

    def describe_clear_queue():

        def it_clears_the_queue(room):
            room.add_card("John Doe", Color.green)

            room.clear_queue()

            expect(room.queue) == []

        def it_handles_empty_queues(room):
            room.clear_queue()

            expect(room.queue) == []
