class Card(dict):
    """Represents a colored card raised by a person."""

    def __init__(self, name, color):
        super(Card, self).__init__()
        self['name'] = name
        self['color'] = color

    def __repr__(self):
        return dict.__repr__(self)
