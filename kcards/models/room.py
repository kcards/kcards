import time
from collections import OrderedDict
import logging

from ..extensions import db
from ..extensions import rw

from .card import Card
from .color import Color


log = logging.getLogger(__name__)


def generate_code():
    """Generate a random string of words for a room code."""
    return '-'.join(generate_simple_words())


def generate_simple_words():
    """Generate a list of three words to use when generating a room code."""
    words = []
    while len(words) < 3:
        word = rw.random_word()
        if is_simple(word):
            words.append(word)
    return words


def is_simple(word):
    """Decide if a word is simple."""
    return len(word) < 7


def get_timestamp():
    """Get the number of seconds since the epoch as an integer."""
    return int(time.time())


class Room(db.Document):
    """Represents a room with card queues."""

    code = db.StringField(primary_key=True, default=generate_code)
    active = db.BooleanField(default=False)
    green = db.ListField(db.StringField())
    yellow = db.ListField(db.StringField())
    red = db.ListField(db.StringField())
    timestamp = db.IntField(default=get_timestamp)

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
        content['timestamp'] = self.timestamp
        return content

    @property
    def queue(self):
        items = []

        for name in self.red:
            items.append(Card(name, Color.red))

        if self.active:

            for name in self.yellow:
                items.append(Card(name, Color.yellow))

            for name in self.green:
                items.append(Card(name, Color.green))

        else:

            for name in self.green[:1]:
                items.append(Card(name, Color.green))

            for name in self.yellow:
                items.append(Card(name, Color.yellow))

            for name in self.green[1:]:
                items.append(Card(name, Color.green))

        return items

    def clean(self):
        """Automatically called before `Document.save()`."""
        self.code = self.clean_code(self.code)

    @staticmethod
    def clean_code(string):
        """Remove spaces from room codes."""
        return '-'.join(string.lower().split()) if string else None

    def add_card(self, name, color):
        """Add a card to the room's queue."""
        if color == Color.yellow and not self.green:
            self.active = True

        if color == Color.green and not self.yellow:
            self.active = False

        getattr(self, color.name).append(name)

        self.timestamp = get_timestamp()

    def next_speaker(self):
        """Remove the current speaker from the queue."""
        if not any((self.green, self.yellow, self.red)):
            return

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

        self.timestamp = get_timestamp()

    def clear_queue(self):
        """Reset the whole speaker queue."""
        del self.green[:]
        del self.yellow[:]
        del self.red[:]

        self.timestamp = get_timestamp()

    @classmethod
    def cleanup(cls, max_age=(3 * 7 * 24 * 60 * 60)):
        """Delete rooms older than the maximum allowed age."""
        log.info("Deleting rooms older than %s seconds", max_age)
        now = get_timestamp()
        for room in cls.objects():
            age = now - room.timestamp
            if age > max_age:
                log.info("Deleting %r at %s seconds", room, age)
                room.delete()
                yield room
            else:
                log.info("Keeping %r at %s seconds", room, age)
