# pylint: disable=unused-variable,unused-argument,expression-not-assigned

from expecter import expect

from .utils import load


def describe_root():

    def describe_GET():

        def it_returns_metadata(client):
            status, content = load(client.get("/api"))

            expect(status) == 200
            expect(content) == {
                'rooms': "http://localhost/api/rooms/"
            }


def describe_rooms_index():

    def describe_GET():

        def it_returns_a_list_of_rooms(client, room):
            status, content = load(client.get("/api/rooms/"))

            expect(status) == 200
            expect(content).contains(
                "http://localhost/api/rooms/foobar"
            )

    def describe_POST():

        def it_creates_a_new_room(client):
            status, content = load(client.post("/api/rooms/"))

            expect(status) == 201

        def the_code_can_be_specified(client):
            params = {'code': '1234'}
            status, content = load(client.post("/api/rooms/", data=params))

            expect(status) == 201
            expect(content['code']) == "1234"

        def numerical_codes_are_converted_to_strings(client):
            params = {'code': 0}
            status, content = load(client.post("/api/rooms/", data=params))

            expect(status) == 201
            expect(content['code']) == "0"

        def using_an_existing_code_returns_an_error(client, room):
            params = {'code': 'foobar'}
            status, content = load(client.post("/api/rooms/", data=params))

            expect(status) == 409
            expect(content['message']) == "This room already exists."


def describe_rooms_detail():

    def describe_GET():

        def it_returns_metadata_for_the_room(client, room):
            status, content = load(client.get("/api/rooms/foobar"))

            expect(status) == 200

        def it_returns_404_on_unknown_rooms(client):
            status, content = load(client.get("/api/rooms/unknown"))

            expect(status) == 404

    def describe_DELETE():

        def it_deletes_the_room(client, room):
            status, content = load(client.delete("/api/rooms/foobar"))

            expect(status) == 204


def describe_rooms_queue():

    def describe_GET():

        def it_returns_the_rooms_queue(client, room):
            room.yellow.append("John Doe")
            room.red.append("Jane Doe")
            room.save()

            status, content = load(client.get("/api/rooms/foobar/queue"))

            expect(status) == 200
            expect(content['queue']) == [
                {
                    'color': 'red',
                    'name': "Jane Doe",
                },
                {
                    'color': 'yellow',
                    'name': "John Doe",
                },
            ]

    def describe_POST():

        def it_adds_to_the_queue(client, room):
            params = {'color': 'yellow',
                      'name': "John Doe"}
            status, content = load(client.post("/api/rooms/foobar/queue",
                                               data=params))
            expect(status) == 202
            expect(content['queue']) == [
                {
                    'color': 'yellow',
                    'name': "John Doe",
                },
            ]

        def it_returns_404_on_unknown_rooms(client):
            status, content = load(client.post("/api/rooms/unknown/queue"))

            expect(status) == 404
