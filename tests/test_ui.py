# pylint: disable=unused-variable,unused-argument

from expecter import expect

from .utils import post


def describe_join():

    def it_requires_a_name(client, room):
        data = {'name': ""}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("A name is required.")

    def it_trims_whitespace_on_names(client, room):
        data = {'name': "  Jace "}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("Welcome, Jace!")
