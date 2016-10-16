#!/usr/bin/env python

import os

from kcards.settings import get_config
from kcards.app import create_app
from kcards import models


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    models.Room(code='_new').save()


if __name__ == '__main__':
    main()
