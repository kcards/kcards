# pylint: disable=unused-variable,unused-argument,expression-not-assigned

from expecter import expect

from .utils import load


def describe_root():

    def describe_GET():

        def it_returns_metadata(client):
            status, data = load(client.get("/api"))

            expect(status) == 200
            expect(data) == {
                'rooms': "http://localhost/api/rooms/"
            }


def describe_rooms_index():

    def describe_GET():

        def it_returns_a_list_of_rooms(client, room):
            status, data = load(client.get("/api/rooms/"))

            expect(status) == 200
            expect(data) == [
                "http://localhost/api/rooms/foobar"
            ]


def describe_rooms_detail():

    def describe_GET():

        def it_returns_metadata_for_the_room(client, room):
            status, data = load(client.get("/api/rooms/foobar"))

            expect(status) == 200

        def it_returns_404_on_unknown_rooms(client):
            status, data = load(client.get("/api/rooms/unknown"))

            expect(status) == 404
