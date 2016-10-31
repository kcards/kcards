from enum import Enum


class Color(str, Enum):
    change = 'green'
    followup = 'yellow'
    interrupt = 'red'
