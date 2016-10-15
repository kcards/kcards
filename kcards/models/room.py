from ..extensions import db


class Room(db.Document):
    _id = db.StringField(required=True)

    def __str__(self):
        return self.code

    def __eq__(self, other):
        return self.code == other.code

    def __lt__(self, other):
        return self.code < other.code

    @property
    def code(self):
        return self._id

    @property
    def data(self):
        return {'code': self.code}
