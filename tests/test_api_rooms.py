# pylint: disable=unused-variable,unused-argument,expression-not-assigned

from expecter import expect

from kcards.models import Room

from .utils import load


def describe_index():

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

        def spaces_are_converted_to_dashes(client):
            params = {'code': ' some   spaces here'}
            status, content = load(client.post("/api/rooms/", data=params))

            expect(status) == 201
            expect(content['code']) == "some-spaces-here"

        def using_an_existing_code_returns_an_error(client, room):
            params = {'code': 'foobar'}
            status, content = load(client.post("/api/rooms/", data=params))

            expect(status) == 409
            expect(content['message']) == "Room already exists."

    def describe_DELETE():

        def it_deletes_older_rooms(client):
            Room(code='newer').save()
            Room(code='older', timestamp=12345).save()

            status, content = load(client.delete("/api/rooms/"))

            expect(status) == 200
            expect(content) == [
                "older"
            ]


def describe_detail():

    def describe_GET():

        def it_returns_metadata_for_the_room(client, room):
            status, content = load(client.get("/api/rooms/foobar"))

            expect(status) == 200

        def it_returns_404_on_unknown_rooms(client):
            status, content = load(client.get("/api/rooms/unknown"))

            expect(status) == 404
            expect(content) == {
                'message': "Room not found: unknown"
            }

    def describe_DELETE():

        def it_deletes_the_room(client, room):
            status, content = load(client.delete("/api/rooms/foobar"))

            expect(status) == 204


def describe_detail_timestamp():

    def describe_GET():

        def it_returns_a_single_value(client, room):
            status, content = load(client.get("/api/rooms/foobar/timestamp"))

            expect(status) == 200
            expect(content) == {'timestamp': 1478683992}


def describe_detail_queue():

    def describe_GET():

        def it_returns_the_rooms_queue(client, populated_room):
            status, content = load(client.get("/api/rooms/foobar/queue"))

            expect(status) == 200
            expect(content['queue']) == [
                {
                    'name': "Jace Browning",
                    'color': '#BF1A2F',
                },
                {
                    'name': "John Doe",
                    'color': '#018E42',
                },
                {
                    'name': "Bob Smith",
                    'color': '#F7D002',
                },
                {
                    'name': "Dan Lindeman",
                    'color': '#018E42',
                },
            ]

    def describe_POST():

        def it_adds_to_the_queue(client, room):
            params = {'color': 'yellow',
                      'name': "John Doe"}
            status, content = load(client.post("/api/rooms/foobar/queue",
                                               data=params))
            expect(status) == 200
            expect(content['queue']) == [
                {
                    'color': '#F7D002',
                    'name': "John Doe",
                },
            ]

        def it_returns_404_on_unknown_rooms(client):
            status, content = load(client.post("/api/rooms/unknown/queue"))

            expect(status) == 404

        def it_returns_422_when_missing_params(client, room):
            status, content = load(client.post("/api/rooms/foobar/queue"))

            expect(status) == 422
            expect(content) == {
                'message': "Name and color are required.",
            }

    def describe_DELETE():

        def it_clears_the_queue(client, populated_room):
            status, content = load(client.delete("/api/rooms/foobar/queue"))

            expect(status) == 200
            expect(content['queue']) == []

        def it_returns_404_on_unknown_rooms(client):
            status, content = load(client.delete("/api/rooms/unknown/queue"))

            expect(status) == 404


def describe_detail_next():

    def describe_POST():

        def it_allows_current_speaker_to_hit_next(client, populated_room):
            params = {'color': 'red',
                      'name': "Jace Browning"}
            status, content = load(client.post("/api/rooms/foobar/next",
                                               data=params))
            expect(status) == 200
            expect(content['queue']) == [
                {
                    'name': "John Doe",
                    'color': '#018E42',
                },
                {
                    'name': "Bob Smith",
                    'color': '#F7D002',
                },
                {
                    'name': "Dan Lindeman",
                    'color': '#018E42',
                },
            ]

        def non_speakers_are_ignored(client, populated_room):
            params = {'color': 'yellow',
                      'name': "John Doe"}
            status, content = load(client.post("/api/rooms/foobar/next",
                                               data=params))
            expect(status) == 200
            expect(content['queue']) == [
                {
                    'name': "Jace Browning",
                    'color': '#BF1A2F',
                },
                {
                    'name': "John Doe",
                    'color': '#018E42',
                },
                {
                    'name': "Bob Smith",
                    'color': '#F7D002',
                },
                {
                    'name': "Dan Lindeman",
                    'color': '#018E42',
                },
            ]

        def it_returns_422_when_missing_params(client, room):
            status, content = load(client.post("/api/rooms/foobar/next"))

            expect(status) == 422
            expect(content) == {
                'message': "Name required.",
            }
