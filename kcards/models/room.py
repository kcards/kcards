import random
from collections import OrderedDict

from ..extensions import db

from .card import Card
from .color import Color


CODE_ALPHABET = "bcdfghjklmnpqrstvwxyz"


def generate_code(length=6):
    """Generate a random string of characters for a room code."""
    return ''.join(random.choice(CODE_ALPHABET) for _ in range(length))


class Room(db.Document):
    """Represents a room with card queues."""

    code = db.StringField(primary_key=True, default=generate_code)
    active = db.BooleanField(default=False)
    change = db.ListField(db.StringField())
    followup = db.ListField(db.StringField())
    interrupt = db.ListField(db.StringField())

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

        for name in self.interrupt:
            items.append(Card(name, Color.interrupt))

        if self.active:

            for name in self.followup:
                items.append(Card(name, Color.followup))

            for name in self.change:
                items.append(Card(name, Color.change))

        else:

            for name in self.change[:1]:
                items.append(Card(name, Color.change))

            for name in self.followup:
                items.append(Card(name, Color.followup))

            for name in self.change[1:]:
                items.append(Card(name, Color.change))

        return items

    def add_card(self, name, color):
        """Add a card to the room's queue."""
        if color == Color.followup and not self.change:
            self.active = True

        if color == Color.change and not self.followup:
            self.active = False

        getattr(self, color.name).append(name)

    def next_speaker(self):
        """Remove the current speaker from the queue."""
        if self.interrupt:
            self.interrupt.pop(0)

        elif self.change and not self.active:
            self.change.pop(0)
            if self.followup:
                self.active = True

        elif self.followup:
            self.followup.pop(0)
            if not self.followup:
                self.active = False
