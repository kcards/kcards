#!/usr/bin/env python

import os

from kcards.settings import get_config
from kcards.app import create_app
from kcards import models


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    room = models.Room(code='_0_new_room')
    room.save()

    room = models.Room(code='_1_new_topic')
    room.yellow.append("John Doe")
    room.green.append("Dan Lindeman")
    room.yellow.append("Jace Browning")
    room.save()

    room = models.Room(code='_2_active_discussion')
    room.active = True
    room.yellow.append("John Doe")
    room.green.append("Dan Lindeman")
    room.yellow.append("Jace Browning")
    room.save()

    room = models.Room(code='_3_red_card')
    room.active = True
    room.yellow.append("John Doe")
    room.green.append("Dan Lindeman")
    room.yellow.append("Jace Browning")
    room.red.append("Mr. Timekeeper")
    room.save()


if __name__ == '__main__':
    main()
