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
            expect(data).contains(
                "http://localhost/api/rooms/foobar"
            )

    def describe_POST():

        def it_creates_a_new_room(client):
            status, data = load(client.post("/api/rooms/"))

            expect(status) == 201

        def the_code_can_be_specified(client):
            params = {'code': '1234'}
            status, data = load(client.post("/api/rooms/", data=params))

            expect(status) == 201
            expect(data) == {
                'uri': "http://localhost/api/rooms/1234"
            }

        def numberical_codes_are_converted_to_strings(client):
            params = {'code': 0}
            status, data = load(client.post("/api/rooms/", data=params))

            expect(status) == 201
            expect(data) == {
                'uri': "http://localhost/api/rooms/0"
            }


def describe_rooms_detail():

    def describe_GET():

        def it_returns_metadata_for_the_room(client, room):
            status, data = load(client.get("/api/rooms/foobar"))

            expect(status) == 200

        def it_returns_404_on_unknown_rooms(client):
            status, data = load(client.get("/api/rooms/unknown"))

            expect(status) == 404

    def describe_DELETE():

        def it_deletes_the_room(client, room):
            status, data = load(client.delete("/api/rooms/foobar"))

            expect(status) == 204
