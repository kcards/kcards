#!/usr/bin/env python

import os

from kcards.settings import get_config
from kcards.app import create_app
from kcards import models


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    new = models.Room(code='_0_new')
    new.save()

    started = models.Room(code='_1_started')
    started.green.append("Dan Lindeman")
    started.green.append("Jace Browning")
    started.yellow.append("John Doe")
    started.save()

    started = models.Room(code='_2_redcard')
    started.green.append("Dan Lindeman")
    started.green.append("Jace Browning")
    started.yellow.append("John Doe")
    started.red.append("Mr. Timekeeper")
    started.save()


if __name__ == '__main__':
    main()
