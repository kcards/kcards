# pylint: disable=unused-variable,unused-argument

from expecter import expect

from kcards.models import Room

from .utils import get, post


def describe_index():

    def describe_create():

        def with_code(client):
            data = dict(create=True, code="foobar")
            html = post(client, "/", data)

            expect(html).contains("What is your name?")
            expect(html).contains("foobar")

        def with_spaces_in_code(client):
            data = dict(create=True, code="foo bar")
            html = post(client, "/", data)

            expect(html).contains("What is your name?")
            expect(html).contains("foo-bar")

        def without_code(client):
            data = dict(create=True)
            html = post(client, "/", data)

            expect(html).contains("What is your name?")
            expect(html).contains("-")  # generated room code

    def describe_goto():

        def with_code(client, room):
            data = dict(goto=True, code=room.code)
            html = post(client, "/", data)

            expect(html).contains("What is your name?")
            expect(html).contains(room.code)

        def with_unknown_code(client):
            data = dict(goto=True, code="unknown")
            html = post(client, "/", data)

            expect(html).contains("Room not found: unknown")

        def with_spaces_in_code(client):
            Room(code='foo-bar').save()

            data = dict(goto=True, code="foo bar")
            html = post(client, "/", data)

            expect(html).contains("What is your name?")
            expect(html).contains("foo-bar")

        def without_code(client):
            data = dict(goto=True, code="")
            html = post(client, "/", data)

            expect(html).contains("Room code is required.")

        def with_only_spaces(client):
            data = dict(goto=True, code="   ")
            html = post(client, "/", data)

            expect(html).contains("Room code is required.")


def describe_rooms_detail():

    # pylint: disable=line-too-long

    def with_unknown_code(client):
        html = get(client, "/rooms/unknown")

        expect(html).contains("Room not found: unknown")

    def when_empty_queue(client, room):
        html = get(client, "/rooms/foobar?name=Some+Guy")
        expect(html).contains('<input type="submit" class="btn btn-default disabled" name="next"')

    def next_speaker_when_current(client, populated_room):
        html = get(client, "/rooms/foobar?name=Jace+Browning")
        expect(html).contains('<input type="submit" class="btn btn-default" name="next"')

    def next_speaker_when_not_current(client, populated_room):
        html = get(client, "/rooms/foobar?name=Dan+Lindeman")
        expect(html).contains('<input type="submit" class="btn btn-default disabled" name="next"')


def describe_rooms_detail_join():

    def with_name(client, room):
        data = {'name': "Jace"}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("Welcome, Jace!")

    def with_name_and_extra_spaces(client, room):
        data = {'name': "  Jace "}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("Welcome, Jace!")

    def without_name(client, room):
        data = {'name': ""}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("A name is required.")


def describe_rooms_detail_options():

    def describe_change_name():

        def with_name(client, room):
            data = dict(rename=True, name="New Name")
            html = post(client, "/rooms/foobar/options", data)

            expect(html).contains("Name changed: New Name")

        def with_name_and_extra_spaces(client, room):
            data = dict(rename=True, name=" New Name ")
            html = post(client, "/rooms/foobar/options", data)

            expect(html).contains("Name changed: New Name")

        def without_name(client, room):
            data = dict(rename=True, name="")
            html = post(client, "/rooms/foobar/options", data)

            expect(html).contains("A name is required.")

    def describe_back():

        def with_button_click(client, room):
            data = dict()
            html = post(client, "/rooms/foobar/options", data)

            expect(html).contains("foobar")
