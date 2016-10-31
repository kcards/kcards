# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from kcards.models import Room, Card, Color


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
                Card("John", Color.followup),
                Card("Fred", Color.followup),
                Card("Bob", Color.change),
                Card("Joe", Color.change),
            ]

        def when_inactive(filled_room):
            filled_room.active = False

            expect(filled_room.queue) == [
                Card("Bob", Color.change),
                Card("John", Color.followup),
                Card("Fred", Color.followup),
                Card("Joe", Color.change),
            ]

    def describe_add_card():

        def with_single_card(room):
            room.add_card("John Doe", Color.change)

            expect(room.queue) == [
                Card("John Doe", Color.change),
            ]

        def with_multiple_cards(room):
            room.add_card("John Doe", Color.followup)
            room.add_card("Jace Browning", Color.change)
            room.add_card("Dan Lindeman", Color.followup)

            expect(room.queue) == [
                Card("John Doe", Color.followup),
                Card("Dan Lindeman", Color.followup),
                Card("Jace Browning", Color.change),
            ]

        def with_red_card(room):
            room.add_card("John Doe", Color.change)
            room.add_card("Jace Browning", Color.followup)
            room.add_card("Dan Lindeman", Color.interrupt)

            expect(room.queue) == [
                Card("Dan Lindeman", Color.interrupt),
                Card("John Doe", Color.change),
                Card("Jace Browning", Color.followup),
            ]

    def describe_next_speaker():

        def it_does_not_remove_from_empty(room):
            room.next_speaker()

            expect(room.queue) == []

        def it_removes_the_red_speaker_first(room):
            room.add_card("John Doe", Color.change)
            room.add_card("Jace Browning", Color.interrupt)

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", Color.change),
            ]

        def it_starts_a_new_thread(room):
            room.add_card("Jace Browning", Color.change)
            room.add_card("John Doe", Color.followup)

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", Color.followup),
            ]

        def it_removes_the_next_followup(room):
            room.add_card("Jace Browning", Color.followup)
            room.add_card("Dan Lindeman", Color.followup)

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", Color.followup)
            ]

        def it_removes_the_last_followup(room):
            room.add_card("John Doe", Color.followup)
            room.add_card("Jace Browning", Color.change)

            room.next_speaker()

            expect(room.queue) == [
                Card("Jace Browning", Color.change),
            ]

        def it_removes_the_current_topic(room):
            room.add_card("John Doe", Color.change)
            room.add_card("Jace Browning", Color.followup)
            room.add_card("Dan Lindeman", Color.change)

            room.next_speaker()

            expect(room.queue) == [
                Card("Jace Browning", Color.followup),
                Card("Dan Lindeman", Color.change),
            ]

        def it_removes_the_green_speaker_if_only_greens_are_queued(room):
            room.add_card("John Doe", Color.change)
            room.add_card("Dan Lindeman", Color.change)

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", Color.change),
            ]

        def it_clears_the_queue_without_active_discussion(room):
            room.add_card("John Doe", Color.change)
            room.add_card("Dan Lindeman", Color.change)

            room.next_speaker()
            room.next_speaker()

            expect(room.queue) == []

        def it_clears_the_queue_with_active_discussion(room):
            room.add_card("John Doe", Color.change)
            room.add_card("Jace Browning", Color.followup)
            room.add_card("Dan Lindeman", Color.change)

            room.next_speaker()
            room.next_speaker()
            room.next_speaker()

            expect(room.queue) == []
