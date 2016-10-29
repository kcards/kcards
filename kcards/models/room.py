import random
from collections import OrderedDict

from ..extensions import db


CODE_ALPHABET = "bcdfghjklmnpqrstvwxyz"


def generate_code(length=6):
    """Generate a random string of characters for a room code."""
    return ''.join(random.choice(CODE_ALPHABET) for _ in range(length))


class Room(db.Document):
    """Represents a room with card queues."""

    code = db.StringField(primary_key=True, default=generate_code)
    active = db.BooleanField(default=False)
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
        content = OrderedDict()
        content['uri'] = None  # to be set in views
        content['code'] = self.code
        content['queue'] = self.queue
        return content

    @property
    def queue(self):
        items = []

        for name in self.red:
            items.append(Card(name, 'red'))

        if self.active:

            for name in self.yellow:
                items.append(Card(name, 'yellow'))

            for name in self.green:
                items.append(Card(name, 'green'))

        else:

            for name in self.green[:1]:
                items.append(Card(name, 'green'))

            for name in self.yellow:
                items.append(Card(name, 'yellow'))

            for name in self.green[1:]:
                items.append(Card(name, 'green'))

        return items

    def add(self, name, color):
        """Add a card to the room's queue."""
        if color == 'yellow' and not self.green:
            self.active = True

        if color == 'green' and not self.yellow:
            self.active = False

        getattr(self, color).append(name)

    def next_speaker(self):
        """Remove the current speaker from the queue."""
        if self.red:
            self.red.pop(0)

        elif self.green and not self.active:
            self.green.pop(0)
            if self.yellow:
                self.active = True

        elif self.yellow:
            self.yellow.pop(0)
            if not self.yellow:
                self.active = False


class Card(OrderedDict):
    """Represents a colored card raised by a person."""

    def __init__(self, name, color):
        super(Card, self).__init__()
        self['name'] = name
        self['color'] = color

    def __repr__(self):
        return dict.__repr__(self)
