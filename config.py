import os


class Configuration(object):
    DEBUG = True
    SECRET_KEY = "RANDOM_KEY" # нужно будет придумать что получше
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "app", "main.db")
