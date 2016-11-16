# pylint: disable=unused-variable,unused-argument

from expecter import expect

from kcards.models import Room

from .utils import post


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

    def describe_goto():

        def with_code(client, room):
            data = dict(goto=True, code=room.code)
            html = post(client, "/", data)

            expect(html).contains("What is your name?")
            expect(html).contains(room.code)

        def with_unknown_code(client):
            data = dict(goto=True, code="unknown")
            html = post(client, "/", data)

            expect(html).contains("I don't know about that room.")

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


def describe_join():

    def it_requires_a_name(client, room):
        data = {'name': ""}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("A name is required.")

    def it_trims_whitespace_on_names(client, room):
        data = {'name': "  Jace "}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("Welcome, Jace!")
