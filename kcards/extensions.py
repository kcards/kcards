from flask_mongoengine import MongoEngine
from random_words import RandomWords
from flask_bootstrap import Bootstrap

db = MongoEngine()
rw = RandomWords()
bootstrap = Bootstrap()
