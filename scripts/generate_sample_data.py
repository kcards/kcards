#!/usr/bin/env python

import os

from kcards.settings import get_config
from kcards.app import create_app
from kcards.models import Room, Color


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    room = Room(code='_0_new_room')
    room.save()

    room = Room(code='_1_new_topic')
    room.change = ["John Doe", "Jace Browning"]
    room.followup = ["Dan Lindeman"]
    room.save()

    room = Room(code='_2_active_discussion')
    room.active = True
    room.change = ["John Doe", "Jace Browning"]
    room.followup = ["Dan Lindeman"]
    room.save()

    room = Room(code='_3_red_card')
    room.active = True
    room.change = ["John Doe", "Jace Browning"]
    room.followup = ["Dan Lindeman"]
    room.interrupt = ["Mr. Timekeeper"]
    room.save()


if __name__ == '__main__':
    main()
