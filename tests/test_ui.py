# pylint: disable=unused-variable,unused-argument

from expecter import expect

from .utils import post


def describe_join():

    def it_trims_whitespace_on_names(client, room):
        data = {'name': "  Jace "}
        html = post(client, "/rooms/foobar/join", data)

        expect(html).contains("Welcome, Jace!")
