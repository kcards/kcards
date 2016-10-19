from collections import OrderedDict


class OrderedAttributeDict(OrderedDict):
    """An ordered dictionary with keys available as attributes."""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
