import random

from ..extensions import db


CODE_ALPHABET = "bcdfghjklmnpqrstvwxyz"


def generate_code(length=6):
    """Generate a random string of characters for a room code."""
    return ''.join(random.choice(CODE_ALPHABET) for _ in range(length))


class Room(db.Document):
    code = db.StringField(primary_key=True, default=generate_code)
    green = db.ListField(db.StringField())
    yellow = db.ListField(db.StringField())
    red = db.ListField(db.StringField())

    def __str__(self):
        return self.code

    def __eq__(self, other):
        return self.code == other.code

    def __lt__(self, other):
        return self.code < other.code

    @property
    def data(self):
        return {'code': self.code,
                'queue': self.queue}

    @property
    def queue(self):
        items = []

        for name in self.red:
            items.append({'color': 'red',
                          'name': name})

        for name in self.green:
            items.append({'color': 'green',
                          'name': name})

        for name in self.yellow:
            items.append({'color': 'yellow',
                          'name': name})

        return items
