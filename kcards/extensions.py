from flask_mongoengine import MongoEngine
from random_words import RandomWords
from flask_bootstrap import Bootstrap
from flask_nav import Nav

db = MongoEngine()
rw = RandomWords()

bootstrap = Bootstrap()
nav = Nav()
