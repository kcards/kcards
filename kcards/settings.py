import os


class Config:
    """Base configuration."""

    ENV = None

    PATH = os.path.abspath(os.path.dirname(__file__))
    ROOT = os.path.dirname(PATH)
    DEBUG = False
    THREADED = False


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'

    MONGO_URI = os.getenv('MONGODB_URI')


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'

    DEBUG = True
    TESTING = True

    MONGO_DBNAME = 'kcards_test'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'

    DEBUG = True

    # TODO: this doesn't seem to be taking effect
    # https://github.com/kcards/kcards/issues/5
    MONGO_DBNAME = 'kcards_dev'


def get_config(name):
    assert name, "no configuration specified"

    for config in Config.__subclasses__():  # pylint: disable=no-member
        if config.ENV == name:
            return config

    assert False, "no matching configuration"
