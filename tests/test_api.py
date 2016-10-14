# pylint: disable=unused-variable,expression-not-assigned

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
