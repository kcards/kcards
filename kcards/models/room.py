from ..extensions import db


class Room(db.Document):
    _id = db.StringField(required=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    @property
    def name(self):
        return self._id

    @property
    def data(self):
        return {
            'name': self.name
        }
